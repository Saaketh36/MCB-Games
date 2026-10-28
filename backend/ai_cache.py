"""
AI Question Bank Cache for MyClassboard Games Platform.
Provides database-backed caching in PostgreSQL with intelligent topic matching
to ensure fast, zero-quota question retrieval for similar classes and topics.
"""

import re
import json
import logging
from datetime import datetime
from backend.models import db, CachedAiTask

logger = logging.getLogger("ai_cache")


def normalize_topic_key(text):
    """Normalize topic string for fuzzy/normalized cache indexing."""
    if not text:
        return ""
    # Lowercase and extract alphanumeric words
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', str(text).lower())
    ignore_words = {'the', 'and', 'for', 'with', 'about', 'quiz', 'game', 'test', 'class', 'grade', 'student', 'kids'}
    words = [w for w in cleaned.split() if len(w) > 2 and w not in ignore_words]
    return "_".join(sorted(words)) if words else cleaned.strip().replace(" ", "_")


def build_cache_key(class_name, subject, topic, difficulty="Medium", num_questions=3):
    """Generate standardized cache key."""
    c = str(class_name or "IV").strip().upper()
    s = str(subject or "Science").strip().lower()
    t = normalize_topic_key(topic)
    d = str(difficulty or "Medium").strip().lower()
    n = max(1, int(num_questions or 3))
    return f"{c}:{s}:{t}:{d}:{n}"


def lookup_cached_task(session, class_name, subject, topic, difficulty="Medium", num_questions=3):
    """
    Search PostgreSQL for a matching cached question pack.
    Returns (task_data_dict, provider_string) or None if not found.

    CRITICAL RULES TO PREVENT CROSS-DIFFICULTY & TRUNCATED REPETITION:
    1. Difficulty MUST match strictly. An Easy task must NEVER be returned for Medium/Challenging,
       and a Challenging task must NEVER be returned for Easy.
    2. Question count: A cached pack must contain AT LEAST the requested number of questions.
       If user requests 5 or 8 questions, a cached 3-question pack MUST NOT be returned!
    3. Topic matching: Must match key concepts precisely, avoiding false matches across unrelated topics.
    """
    try:
        req_class = str(class_name or "IV").strip().upper()
        req_subject = str(subject or "Science").strip()
        req_diff = str(difficulty or "Medium").strip().lower()
        req_num = max(1, int(num_questions or 3))
        norm_t = normalize_topic_key(topic)

        if not norm_t:
            return None

        primary_key = build_cache_key(req_class, req_subject, topic, req_diff, req_num)

        # 1. Exact Key Match (Exact class, subject, topic, difficulty, and count)
        record = session.query(CachedAiTask).filter_by(cache_key=primary_key).first()
        if record:
            task_dict = json.loads(record.task_data) if isinstance(record.task_data, str) else record.task_data
            qs = task_dict.get('questions', [])
            # Verify actual question count in payload satisfies the requested count
            if len(qs) >= req_num:
                record.hit_count = (record.hit_count or 1) + 1
                record.updated_at = datetime.utcnow()
                session.commit()
                if len(qs) > req_num:
                    task_dict['questions'] = qs[:req_num]
                    task_dict['time'] = f"{max(3, req_num * 2)} min"
                logger.info(f"Cache hit (exact) for key: {primary_key} (hits: {record.hit_count})")
                return task_dict, record.provider

        # 2. Match Cached Tasks for the SAME Class, Subject, and DIFFICULTY
        # MUST filter by difficulty so Easy doesn't match Challenging/Medium!
        candidates = session.query(CachedAiTask).filter(
            CachedAiTask.class_name == req_class,
            CachedAiTask.subject.ilike(req_subject),
            db.func.lower(CachedAiTask.difficulty) == req_diff
        ).all()

        words_req = set(norm_t.split('_'))

        for cand in candidates:
            cand_norm = normalize_topic_key(cand.topic)
            words_cand = set(cand_norm.split('_'))

            if not words_req or not words_cand:
                continue

            # Topic matching condition:
            # Exact set match OR high Jaccard similarity (>= 0.75)
            intersection = words_req.intersection(words_cand)
            union = words_req.union(words_cand)
            similarity = len(intersection) / len(union) if union else 0.0

            is_topic_match = (words_req == words_cand) or (similarity >= 0.75)
            if not is_topic_match:
                continue

            task_dict = json.loads(cand.task_data) if isinstance(cand.task_data, str) else cand.task_data
            cand_qs = task_dict.get('questions', [])

            # CRITICAL CHECK: Does this cached pack have AT LEAST the requested number of questions?
            # If user asks for 5 or 8, and candidate only has 3 -> SKIP (Cache Miss)!
            if len(cand_qs) < req_num:
                logger.info(f"Cache candidate '{cand.cache_key}' has only {len(cand_qs)} questions, requested {req_num}. Treating as cache miss.")
                continue

            # Candidate satisfies the topic, difficulty, and has sufficient questions!
            cand.hit_count = (cand.hit_count or 1) + 1
            cand.updated_at = datetime.utcnow()
            session.commit()

            if len(cand_qs) > req_num:
                task_dict['questions'] = cand_qs[:req_num]
                task_dict['time'] = f"{max(3, req_num * 2)} min"

            logger.info(f"Cache hit (compatible pack): '{cand.cache_key}' for requested {req_num} Qs at {req_diff}")
            return task_dict, cand.provider

        return None
    except Exception as e:
        session.rollback()
        logger.warning(f"Error checking AI task cache: {e}")
        return None


def store_cached_task(session, class_name, subject, topic, difficulty, num_questions, task_data, provider="Gemini"):
    """
    Persist generated question pack into PostgreSQL database.
    """
    try:
        if not task_data or not isinstance(task_data, dict):
            return False

        c = str(class_name or "IV").strip().upper()
        s = str(subject or "Science").strip()
        diff = str(difficulty or "Medium").strip()
        actual_qs = task_data.get('questions', [])
        actual_q_count = len(actual_qs) if actual_qs else max(1, int(num_questions or 3))

        key = build_cache_key(c, s, topic, diff, actual_q_count)
        raw_json = json.dumps(task_data, ensure_ascii=False)

        existing = session.query(CachedAiTask).filter_by(cache_key=key).first()
        if existing:
            existing.task_data = raw_json
            existing.provider = provider
            existing.difficulty = diff
            existing.num_questions = actual_q_count
            existing.updated_at = datetime.utcnow()
        else:
            cached_obj = CachedAiTask(
                cache_key=key,
                class_name=c,
                subject=s,
                topic=str(topic or "")[:150],
                difficulty=diff,
                num_questions=actual_q_count,
                task_data=raw_json,
                provider=str(provider or "Gemini"),
                hit_count=1
            )
            session.add(cached_obj)

        session.commit()
        logger.info(f"Successfully cached AI task in PostgreSQL: {key} ({actual_q_count} Qs, {diff})")
        return True
    except Exception as e:
        session.rollback()
        logger.warning(f"Error persisting AI task to cache: {e}")
        return False


def get_cache_statistics(session):
    """Return summary statistics of the question bank cache."""
    try:
        total_cached = session.query(CachedAiTask).count()
        total_hits = session.query(db.func.sum(CachedAiTask.hit_count)).scalar() or 0
        recent = session.query(CachedAiTask).order_by(CachedAiTask.updated_at.desc()).limit(10).all()
        return {
            'total_cached_tasks': total_cached,
            'total_cache_hits': int(total_hits),
            'recent_topics': [
                {
                    'class': r.class_name,
                    'subject': r.subject,
                    'topic': r.topic,
                    'hits': r.hit_count,
                    'provider': r.provider,
                    'date': r.updated_at.isoformat() if r.updated_at else None
                }
                for r in recent
            ]
        }
    except Exception as e:
        logger.warning(f"Error fetching cache statistics: {e}")
        return {'total_cached_tasks': 0, 'total_cache_hits': 0, 'recent_topics': []}
