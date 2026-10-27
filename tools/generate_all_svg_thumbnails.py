#!/usr/bin/env python3
"""
440-Activity Thematic 3D Diorama SVG Thumbnail Generator.
Generates a bespoke, visually rich, 3D floating island diorama vector illustration
for every single activity in the curriculum catalog (LO-001 through LO-440).
"""

import json
import os
import re
import sys

for s in (sys.stdout, sys.stderr):
    if hasattr(s, 'reconfigure'):
        s.reconfigure(encoding='utf-8', errors='replace')

def match_any(ctx, *patterns):
    for p in patterns:
        p_lower = p.lower()
        if " " in p_lower:
            if p_lower in ctx:
                return True
        else:
            pattern = r'\b' + re.escape(p_lower) + r'(s|es|ed|ing|er|ers)?\b'
            if re.search(pattern, ctx):
                return True
    return False

def get_theme(game):
    gid = game.get('id', '')
    subj = game.get('subject', '')
    skill = game.get('skillArea', '')
    subskill = game.get('subSkillArea', '')
    title = game.get('title', '')
    lo = game.get('learningOutcome', '')

    ctx = f"{skill} {subskill} {title} {lo}".lower()

    # Exact signature overrides
    if gid == 'LO-096' or 'assembly announcement' in ctx or 'lost & found' in ctx:
        return 'announcement_radio'
    if gid == 'LO-097' or 'elephant whisperer' in ctx:
        return 'elephant_safari'
    if gid == 'LO-124' or 'wild adaptation' in ctx or 'claws, teeth' in ctx:
        return 'animal_adaptations'
    if gid == 'LO-125' or 'family reunion' in ctx:
        return 'family_reunion'
    if gid == 'LO-126' or 'botanical wonder' in ctx or 'roots, fruits' in ctx:
        return 'botanical_roots'
    if gid == 'LO-133' or 'school picnic' in ctx:
        return 'school_picnic'
    if gid == 'LO-136' or 'metric converter' in ctx or 'meters and centimeters' in ctx:
        return 'metric_ruler'
    if gid == 'LO-039' or 'cup & bucket' in ctx:
        return 'capacity_water'
    if gid == 'LO-040' or 'play market' in ctx:
        return 'market_money'
    if 'thirsty crow' in ctx:
        return 'thirsty_crow'
    if 'blend express' in ctx:
        return 'blend_express'

    # Subject-based categorizations
    if subj == 'Mathematics':
        if match_any(ctx, 'capacity', 'bucket', 'millilitre', 'litre', 'volume'):
            return 'capacity_water'
        if match_any(ctx, 'money', 'rupee', 'profit', 'loss', 'market', 'cost'):
            return 'market_money'
        if match_any(ctx, 'weight', 'balance', 'kilogram', 'gram', 'heavy'):
            return 'weight_balance'
        if match_any(ctx, 'ruler', 'length', 'distance', 'meter', 'centimeter', 'perimeter', 'area'):
            return 'metric_ruler'
        if match_any(ctx, 'fraction', 'decimal', 'percentage', 'ratio', 'half', 'quarter'):
            return 'fractions_pie'
        if match_any(ctx, 'time', 'clock', 'calendar', 'hour', 'minute'):
            return 'time_clock'
        if match_any(ctx, 'data', 'graph', 'chart', 'tally', 'table', 'pictograph'):
            return 'data_graphs'
        if match_any(ctx, 'algebra', 'equation', 'variable'):
            return 'algebra_balance'
        if match_any(ctx, '3d shape', 'net', 'cube', 'cylinder', 'solid'):
            return 'shapes_3d'
        return 'shapes_geometry'

    if subj == 'English':
        if match_any(ctx, 'phonics', 'letter', 'alphabet', 'sound', 'safari'):
            return 'phonics_book'
        if match_any(ctx, 'listening', 'instruction', 'announcement', 'listen'):
            return 'announcement_radio'
        if match_any(ctx, 'speaking', 'recitation', 'skit', 'rhyme', 'poem', 'oral'):
            return 'speaking_stage'
        if match_any(ctx, 'reading', 'story', 'comprehension', 'passage'):
            return 'treehouse_reading'
        if match_any(ctx, 'grammar', 'parts of speech', 'noun', 'verb', 'sentence'):
            return 'grammar_blocks'
        if match_any(ctx, 'writing', 'punctuation', 'quill', 'dictation'):
            return 'writing_scribe'
        return 'phonics_book'

    if subj in ('Science', 'EVS'):
        if match_any(ctx, 'electric', 'circuit', 'battery', 'bulb'):
            return 'circuits_electric'
        if match_any(ctx, 'magnet', 'pole', 'compass'):
            return 'magnetism'
        if match_any(ctx, 'light', 'mirror', 'prism', 'reflection'):
            return 'optics_prism'
        if match_any(ctx, 'chemical', 'acid', 'base', 'reaction', 'rust'):
            return 'chemistry_lab'
        if match_any(ctx, 'cell', 'microscope', 'microorganism'):
            return 'microscopy_cells'
        if match_any(ctx, 'plant', 'leaf', 'root', 'seed', 'flower', 'photosynthesis'):
            return 'botanical_roots'
        if match_any(ctx, 'animal', 'bird', 'wildlife', 'adaptation', 'claw', 'ear'):
            return 'animal_adaptations'
        if match_any(ctx, 'water', 'rain', 'cycle', 'stream', 'fluid', 'pressure'):
            return 'water_cycle'
        if match_any(ctx, 'environment', 'recycle', 'pollution', 'conservation', 'garden'):
            return 'environment_garden'
        if match_any(ctx, 'family', 'relation', 'grandparent', 'reunion'):
            return 'family_reunion'
        if match_any(ctx, 'picnic', 'food', 'cooking', 'nutrition'):
            return 'school_picnic'
        return 'botanical_roots'

    if subj == 'Social Science':
        if match_any(ctx, 'map', 'globe', 'direction', 'latitude', 'contour'):
            return 'maps_globe'
        if match_any(ctx, 'solar system', 'planet', 'earth', 'space'):
            return 'solar_system'
        if match_any(ctx, 'harappa', 'ancient', 'archaeology'):
            return 'ancient_harappa'
        if match_any(ctx, 'constitution', 'law', 'judiciary', 'justice'):
            return 'constitution_forum'
        if match_any(ctx, 'panchayat', 'election', 'democracy', 'government'):
            return 'panchayat_banyan'
        if match_any(ctx, 'public goods', 'facility', 'transit', 'water, power'):
            return 'public_facilities'
        return 'maps_globe'

    return 'shapes_geometry'

def build_svg(game, theme):
    gid = game.get('id', '')
    title = game.get('title', '')
    subj = game.get('subject', 'General')

    # Color palettes by subject
    sky_colors = {
        'English': ('#E0F2FE', '#BAE6FD', '#7DD3FC'),
        'Mathematics': ('#FEF3C7', '#FDE68A', '#FCD34D'),
        'Science': ('#DCFCE7', '#BBF7D0', '#86EFAC'),
        'EVS': ('#F0FDF4', '#DCFCE7', '#A7F3D0'),
        'Social Science': ('#FEE2E2', '#FECACA', '#FCA5A5'),
    }.get(subj, ('#E0F2FE', '#BAE6FD', '#7DD3FC'))

    sky_top, sky_mid, sky_bot = sky_colors

    # Base SVG template with floating 3D island
    svg_start = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225" width="100%" height="100%">
  <defs>
    <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{sky_top}"/>
      <stop offset="50%" stop-color="{sky_mid}"/>
      <stop offset="100%" stop-color="{sky_bot}"/>
    </linearGradient>
    <radialGradient id="sunGlow" cx="20%" cy="25%" r="35%">
      <stop offset="0%" stop-color="#FFFBEB" stop-opacity="0.95"/>
      <stop offset="40%" stop-color="#FDE68A" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="islandShadow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="islandTop" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80"/>
      <stop offset="100%" stop-color="#16A34A"/>
    </linearGradient>
    <linearGradient id="islandCliff" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#92400E"/>
      <stop offset="35%" stop-color="#78350F"/>
      <stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
    <linearGradient id="waterGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FDE047"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Sky Background (Top-right corner kept clear for UI Assigned badge) -->
  <rect width="400" height="225" fill="url(#skyGrad)"/>
  <circle cx="65" cy="45" r="45" fill="url(#sunGlow)"/>
  <circle cx="65" cy="45" r="18" fill="#FEF08A"/>

  <!-- Soft Clouds (Placed strictly left and center to leave top-right open) -->
  <path d="M 20,65 Q 35,50 55,60 Q 75,45 95,65 Q 105,75 90,85 L 25,85 Z" fill="#FFFFFF" opacity="0.6"/>
  <path d="M 120,40 Q 135,28 150,38 Q 165,25 180,42 Q 190,52 175,60 L 125,60 Z" fill="#FFFFFF" opacity="0.45"/>

  <!-- Ambient Island Drop Shadow -->
  <ellipse cx="200" cy="202" rx="130" ry="16" fill="url(#islandShadow)"/>

  <!-- Floating Green Island Earthen Cliff Base -->
  <path d="M 70,140 C 70,195 330,195 330,140 L 320,165 C 265,198 135,198 80,165 Z" fill="url(#islandCliff)"/>
  <path d="M 90,158 C 140,188 260,188 310,158" stroke="#B45309" stroke-width="2.5" fill="none" opacity="0.4"/>
  <path d="M 115,170 C 160,193 240,193 285,170" stroke="#78350F" stroke-width="2" fill="none" opacity="0.5"/>

  <!-- Floating Green Island Mossy Turf Top -->
  <ellipse cx="200" cy="140" rx="130" ry="32" fill="url(#islandTop)"/>
  <ellipse cx="195" cy="136" rx="115" ry="25" fill="#86EFAC" opacity="0.3"/>

  <!-- Wild Daisies on Turf -->
  <circle cx="105" cy="145" r="3" fill="#FFFFFF"/><circle cx="105" cy="145" r="1.2" fill="#EAB308"/>
  <circle cx="125" cy="155" r="2.5" fill="#FFFFFF"/><circle cx="125" cy="155" r="1" fill="#EAB308"/>
  <circle cx="280" cy="148" r="3" fill="#FFFFFF"/><circle cx="280" cy="148" r="1.2" fill="#EAB308"/>
  <circle cx="295" cy="138" r="2.5" fill="#FFFFFF"/><circle cx="295" cy="138" r="1" fill="#EAB308"/>
'''

    # Scene specific graphics
    theme_graphics = {
        'capacity_water': '''
    <!-- Water Capacity Station (LO-039) -->
    <!-- Yellow Bucket -->
    <path d="M 210,110 L 255,110 L 248,150 L 217,150 Z" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>
    <ellipse cx="232.5" cy="110" rx="22.5" ry="6" fill="#FEF08A"/>
    <ellipse cx="232.5" cy="112" rx="20" ry="5" fill="#38BDF8"/>
    <!-- Bucket Smiley Face -->
    <circle cx="227" cy="128" r="2" fill="#854D0E"/><circle cx="238" cy="128" r="2" fill="#854D0E"/>
    <path d="M 228,135 Q 232.5,140 237,135" stroke="#854D0E" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Translucent Measuring Cup with Pouring Arc -->
    <path d="M 145,95 L 180,90 L 175,130 L 145,130 Z" fill="#BAE6FD" opacity="0.85" stroke="#0284C7" stroke-width="2"/>
    <path d="M 148,105 L 160,105 M 148,115 L 165,115 M 148,123 L 158,123" stroke="#0284C7" stroke-width="1.5"/>
    <path d="M 180,95 Q 205,100 220,112" stroke="#38BDF8" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    <!-- Water Droplet Character -->
    <path d="M 185,138 C 175,138 170,147 185,158 C 200,147 195,138 185,138 Z" fill="#0284C7"/>
    <circle cx="182" cy="146" r="1.2" fill="#FFFFFF"/><circle cx="188" cy="146" r="1.2" fill="#FFFFFF"/>
    <!-- Character Ruler -->
    <rect x="268" y="100" width="12" height="48" rx="2" fill="#FDE047" stroke="#CA8A04" stroke-width="1.5"/>
    <line x1="274" y1="110" x2="280" y2="110" stroke="#854D0E" stroke-width="1.5"/>
    <line x1="274" y1="120" x2="280" y2="120" stroke="#854D0E" stroke-width="1.5"/>
    <line x1="274" y1="130" x2="280" y2="130" stroke="#854D0E" stroke-width="1.5"/>
    <circle cx="272" cy="105" r="1" fill="#854D0E"/><circle cx="276" cy="105" r="1" fill="#854D0E"/>
        ''',

        'market_money': '''
    <!-- Play Market Stall & Coin Characters (LO-040) -->
    <!-- Market Stall Frame & Awning -->
    <rect x="140" y="85" width="6" height="55" fill="#78350F"/>
    <rect x="254" y="85" width="6" height="55" fill="#78350F"/>
    <path d="M 130,85 L 270,85 L 265,65 L 135,65 Z" fill="#EF4444"/>
    <path d="M 130,85 C 140,95 150,95 160,85 C 170,95 180,95 190,85 C 200,95 210,95 220,85 C 230,95 240,95 250,85 C 260,95 270,95 270,85" fill="#FFFFFF" opacity="0.9"/>
    <!-- Wooden Counter & Produce Crates -->
    <rect x="142" y="115" width="116" height="25" fill="#B45309" stroke="#78350F" stroke-width="2"/>
    <rect x="150" y="120" width="25" height="15" fill="#D97706"/>
    <circle cx="156" cy="126" r="4" fill="#EF4444"/><circle cx="166" cy="126" r="4" fill="#EF4444"/>
    <!-- Friendly Gold Coin Character -->
    <circle cx="200" cy="115" r="16" fill="url(#goldGrad)" stroke="#B45309" stroke-width="2"/>
    <circle cx="195" cy="112" r="2.2" fill="#78350F"/><circle cx="205" cy="112" r="2.2" fill="#78350F"/>
    <path d="M 196,118 Q 200,123 204,118" stroke="#78350F" stroke-width="2" fill="none" stroke-linecap="round"/>
    <text x="200" y="138" font-size="9" font-weight="bold" fill="#78350F" text-anchor="middle">₹</text>
    <!-- Velvet Coin Purse -->
    <path d="M 225,135 Q 215,120 235,115 Q 255,120 245,135 Z" fill="#7C3AED" stroke="#5B21B6" stroke-width="2"/>
    <circle cx="235" cy="115" r="3" fill="#FACC15"/>
        ''',

        'announcement_radio': '''
    <!-- School Assembly & Megaphone Announcement (LO-096) -->
    <!-- Vintage Brass Megaphone Speaker on Tripod -->
    <polygon points="150,95 205,75 205,125 150,105" fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <ellipse cx="205" cy="100" rx="8" ry="25" fill="#FDE68A" stroke="#B45309" stroke-width="2"/>
    <line x1="165" y1="105" x2="150" y2="148" stroke="#78350F" stroke-width="3"/>
    <line x1="175" y1="105" x2="195" y2="148" stroke="#78350F" stroke-width="3"/>
    <!-- Soundwaves -->
    <path d="M 220,85 Q 235,100 220,115" stroke="#38BDF8" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M 230,75 Q 250,100 230,125" stroke="#38BDF8" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>
    <!-- Cute Lost & Found Teddy Bear Character -->
    <circle cx="255" cy="130" r="14" fill="#D97706"/>
    <circle cx="245" cy="120" r="5" fill="#B45309"/><circle cx="265" cy="120" r="5" fill="#B45309"/>
    <circle cx="251" cy="128" r="1.5" fill="#451A03"/><circle cx="259" cy="128" r="1.5" fill="#451A03"/>
    <ellipse cx="255" cy="133" rx="4" ry="3" fill="#FDE68A"/>
    <!-- Red Luggage Tag -->
    <polygon points="270,135 285,130 288,142 273,147" fill="#EF4444"/>
    <circle cx="273" cy="138" r="1" fill="#FFFFFF"/>
        ''',

        'elephant_safari': '''
    <!-- Radio Wildlife: Elephant Whisperer (LO-097) -->
    <!-- Cute Baby Elephant -->
    <ellipse cx="185" cy="125" rx="24" ry="18" fill="#94A3B8"/>
    <circle cx="205" cy="115" r="16" fill="#94A3B8"/>
    <ellipse cx="198" cy="112" rx="12" ry="16" fill="#CBD5E1"/>
    <!-- Elephant Trunk -->
    <path d="M 215,118 Q 230,122 225,132 Q 220,136 215,130" stroke="#94A3B8" stroke-width="7" fill="none" stroke-linecap="round"/>
    <circle cx="206" cy="110" r="2" fill="#0F172A"/>
    <!-- Explorer Safari Hat -->
    <ellipse cx="205" cy="102" rx="18" ry="4" fill="#D97706"/>
    <path d="M 193,102 C 193,92 217,92 217,102 Z" fill="#F59E0B"/>
    <!-- Wooden Radio Receiver -->
    <rect x="240" y="120" width="30" height="22" rx="3" fill="#78350F" stroke="#451A03" stroke-width="2"/>
    <line x1="245" y1="120" x2="238" y2="100" stroke="#94A3B8" stroke-width="2"/>
    <circle cx="255" cy="131" r="5" fill="#FDE68A"/>
    <!-- Musical Soundwaves -->
    <path d="M 235,95 Q 242,88 248,94" stroke="#F59E0B" stroke-width="2.5" fill="none"/>
        ''',

        'animal_adaptations': '''
    <!-- Wild Adaptations: Claws, Teeth & Ears (LO-124) -->
    <!-- Tiger Cub Character with Claws -->
    <circle cx="165" cy="120" r="18" fill="#F97316"/>
    <polygon points="152,105 160,110 152,115" fill="#EA580C"/>
    <polygon points="178,105 170,110 178,115" fill="#EA580C"/>
    <circle cx="160" cy="118" r="2" fill="#431407"/><circle cx="170" cy="118" r="2" fill="#431407"/>
    <!-- Paws showing claws -->
    <circle cx="152" cy="134" r="6" fill="#FDBA74"/>
    <line x1="148" y1="130" x2="148" y2="127" stroke="#431407" stroke-width="2"/>
    <line x1="152" y1="129" x2="152" y2="126" stroke="#431407" stroke-width="2"/>
    <line x1="156" y1="130" x2="156" y2="127" stroke="#431407" stroke-width="2"/>
    <!-- Fennec Fox with Giant Ears -->
    <circle cx="235" cy="125" r="16" fill="#FED7AA"/>
    <!-- Giant Ears -->
    <polygon points="220,115 210,80 230,105" fill="#FDBA74" stroke="#FB923C" stroke-width="1.5"/>
    <polygon points="245,115 255,80 238,105" fill="#FDBA74" stroke="#FB923C" stroke-width="1.5"/>
    <circle cx="230" cy="124" r="2" fill="#431407"/><circle cx="240" cy="124" r="2" fill="#431407"/>
    <!-- Eagle Chick with Curved Beak -->
    <circle cx="200" cy="136" r="10" fill="#94A3B8"/>
    <polygon points="208,134 216,137 208,140" fill="#EAB308"/>
        ''',

        'family_reunion': '''
    <!-- Family Reunion: Extended Family Bonds (LO-125) -->
    <!-- Cottage Porch Roof & Festive Bunting -->
    <polygon points="140,80 260,80 250,90 150,90" fill="#991B1B"/>
    <!-- Colorful Bunting Flags -->
    <path d="M 145,95 Q 200,108 255,95" stroke="#64748B" stroke-width="1.5" fill="none"/>
    <polygon points="160,98 170,99 165,108" fill="#EF4444"/>
    <polygon points="180,101 190,102 185,111" fill="#F59E0B"/>
    <polygon points="200,102 210,102 205,111" fill="#10B981"/>
    <polygon points="220,100 230,99 225,108" fill="#3B82F6"/>
    <!-- Grandparent with Spectacles -->
    <circle cx="175" cy="122" r="12" fill="#FED7AA"/>
    <circle cx="170" cy="120" r="3" stroke="#475569" stroke-width="1.5" fill="none"/>
    <circle cx="180" cy="120" r="3" stroke="#475569" stroke-width="1.5" fill="none"/>
    <line x1="173" y1="120" x2="177" y2="120" stroke="#475569" stroke-width="1.5"/>
    <!-- Child Character Hugging -->
    <circle cx="198" cy="128" r="10" fill="#FDBA74"/>
    <circle cx="195" cy="126" r="1.5" fill="#1E293B"/><circle cx="201" cy="126" r="1.5" fill="#1E293B"/>
    <!-- Family Teapot on Table -->
    <ellipse cx="235" cy="138" rx="16" ry="6" fill="#B45309"/>
    <circle cx="235" cy="130" r="7" fill="#E2E8F0"/>
    <path d="M 242,128 Q 248,127 245,133" stroke="#94A3B8" stroke-width="2" fill="none"/>
        ''',

        'botanical_roots': '''
    <!-- Botanical Wonders: Roots & Flowers (LO-126) -->
    <!-- Transparent Soil Box with Growing Carrot Root -->
    <rect x="155" y="115" width="90" height="42" rx="4" fill="#78350F" opacity="0.85" stroke="#451A03" stroke-width="2"/>
    <!-- Growing Orange Carrot in Soil -->
    <polygon points="185,120 195,120 190,152" fill="#F97316"/>
    <line x1="190" y1="130" x2="182" y2="134" stroke="#FB923C" stroke-width="1.5"/>
    <line x1="190" y1="140" x2="198" y2="144" stroke="#FB923C" stroke-width="1.5"/>
    <!-- Green Leaves & Pink Blossom on Top -->
    <path d="M 190,120 C 180,105 170,110 185,115 Z" fill="#22C55E"/>
    <path d="M 190,120 C 200,105 210,110 195,115 Z" fill="#22C55E"/>
    <circle cx="225" cy="105" r="9" fill="#EC4899"/>
    <circle cx="225" cy="105" r="3" fill="#FDE047"/>
    <!-- Miniature Watering Can -->
    <rect x="255" y="125" width="20" height="15" rx="3" fill="#38BDF8"/>
    <path d="M 255,130 L 245,122" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
        ''',

        'school_picnic': '''
    <!-- Everyday Problem Solvers: School Picnic (LO-133) -->
    <!-- Red-and-White Checkered Picnic Blanket -->
    <polygon points="150,140 250,140 270,160 130,160" fill="#FEE2E2" stroke="#EF4444" stroke-width="1.5"/>
    <line x1="170" y1="140" x2="155" y2="160" stroke="#EF4444" stroke-width="2"/>
    <line x1="190" y1="140" x2="180" y2="160" stroke="#EF4444" stroke-width="2"/>
    <line x1="210" y1="140" x2="205" y2="160" stroke="#EF4444" stroke-width="2"/>
    <line x1="230" y1="140" x2="230" y2="160" stroke="#EF4444" stroke-width="2"/>
    <!-- Wicker Picnic Basket -->
    <rect x="160" y="118" width="30" height="20" rx="3" fill="#D97706" stroke="#92400E" stroke-width="2"/>
    <path d="M 160,118 Q 175,108 190,118" stroke="#92400E" stroke-width="2" fill="none"/>
    <!-- Friendly Apple Character -->
    <circle cx="210" cy="132" r="9" fill="#EF4444"/>
    <circle cx="207" cy="130" r="1.2" fill="#FFFFFF"/><circle cx="213" cy="130" r="1.2" fill="#FFFFFF"/>
    <path d="M 210,123 Q 212,118 215,120" stroke="#15803D" stroke-width="2" fill="none"/>
    <!-- Juice Box with Straw -->
    <rect x="228" y="124" width="14" height="18" rx="2" fill="#F59E0B"/>
    <line x1="235" y1="124" x2="238" y2="114" stroke="#F43F5E" stroke-width="2.5" stroke-linecap="round"/>
        ''',

        'metric_ruler': '''
    <!-- Metric Converters: Meters and Centimeters (LO-136) -->
    <!-- Yellow Folding Ruler Character -->
    <rect x="160" y="90" width="14" height="58" rx="3" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>
    <line x1="167" y1="100" x2="174" y2="100" stroke="#854D0E" stroke-width="1.5"/>
    <line x1="167" y1="110" x2="174" y2="110" stroke="#854D0E" stroke-width="1.5"/>
    <line x1="167" y1="120" x2="174" y2="120" stroke="#854D0E" stroke-width="1.5"/>
    <line x1="167" y1="130" x2="174" y2="130" stroke="#854D0E" stroke-width="1.5"/>
    <line x1="167" y1="140" x2="174" y2="140" stroke="#854D0E" stroke-width="1.5"/>
    <!-- Ruler Eyes & Smile -->
    <circle cx="164" cy="96" r="1.5" fill="#713F12"/><circle cx="170" cy="96" r="1.5" fill="#713F12"/>
    <path d="M 164,101 Q 167,104 170,101" stroke="#713F12" stroke-width="1.2" fill="none"/>
    <!-- Coiled Caterpillar Tape Measure Character -->
    <circle cx="210" cy="138" r="10" fill="#38BDF8"/>
    <circle cx="222" cy="136" r="9" fill="#4ADE80"/>
    <circle cx="233" cy="134" r="8" fill="#F43F5E"/>
    <circle cx="230" cy="132" r="1.5" fill="#FFFFFF"/><circle cx="235" cy="132" r="1.5" fill="#FFFFFF"/>
    <!-- Milestone Marker -->
    <rect x="250" y="115" width="22" height="30" rx="4" fill="#E2E8F0" stroke="#94A3B8" stroke-width="2"/>
    <text x="261" y="132" font-size="8" font-weight="bold" fill="#0F172A" text-anchor="middle">1 m</text>
        ''',

        'phonics_book': '''
    <!-- Phonics & Storybook Reading -->
    <!-- Open Storybook -->
    <polygon points="140,115 195,120 195,145 140,140" fill="#FEF08A" stroke="#CA8A04" stroke-width="1.5"/>
    <polygon points="260,115 205,120 205,145 260,140" fill="#FEF08A" stroke="#CA8A04" stroke-width="1.5"/>
    <!-- Floating 3D Character Letters -->
    <text x="160" y="95" font-size="28" font-weight="bold" fill="#EF4444" filter="url(#softGlow)">A</text>
    <text x="195" y="80" font-size="32" font-weight="bold" fill="#3B82F6" filter="url(#softGlow)">B</text>
    <text x="235" y="98" font-size="28" font-weight="bold" fill="#10B981" filter="url(#softGlow)">C</text>
    <!-- Smiling Reading Glasses -->
    <circle cx="185" cy="128" r="8" stroke="#7C3AED" stroke-width="2" fill="#EDE9FE" opacity="0.8"/>
    <circle cx="215" cy="128" r="8" stroke="#7C3AED" stroke-width="2" fill="#EDE9FE" opacity="0.8"/>
    <line x1="193" y1="128" x2="207" y2="128" stroke="#7C3AED" stroke-width="2"/>
        ''',

        'shapes_geometry': '''
    <!-- Geometry & 2D Shapes -->
    <!-- Wooden Tangram Shapes -->
    <polygon points="160,140 195,95 230,140" fill="#3B82F6" stroke="#1D4ED8" stroke-width="2"/>
    <circle cx="240" cy="125" r="16" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>
    <rect x="135" y="115" width="24" height="24" fill="#EF4444" stroke="#B91C1C" stroke-width="2"/>
    <!-- Drafting Compass Drawing Arc -->
    <line x1="200" y1="75" x2="185" y2="115" stroke="#475569" stroke-width="3"/>
    <line x1="200" y1="75" x2="215" y2="115" stroke="#475569" stroke-width="3"/>
    <path d="M 180,120 A 25,25 0 0,1 220,120" stroke="#F43F5E" stroke-width="2" stroke-dasharray="3,3" fill="none"/>
        ''',

        'shapes_3d': '''
    <!-- 3D Shapes & Nets -->
    <!-- Isometric 3D Cube -->
    <polygon points="200,90 230,105 200,120 170,105" fill="#60A5FA"/>
    <polygon points="170,105 200,120 200,150 170,135" fill="#2563EB"/>
    <polygon points="230,105 200,120 200,150 230,135" fill="#1D4ED8"/>
    <!-- 3D Sphere -->
    <circle cx="255" cy="130" r="14" fill="url(#goldGrad)"/>
    <!-- 3D Cone -->
    <polygon points="145,140 160,105 175,140" fill="#F43F5E"/>
    <ellipse cx="160" cy="140" rx="15" ry="5" fill="#BE123C"/>
        ''',

        'fractions_pie': '''
    <!-- Fractions & Bakery Kitchen -->
    <!-- Fraction Pie divided in Quarters -->
    <ellipse cx="200" cy="125" rx="36" ry="16" fill="#FDE68A" stroke="#D97706" stroke-width="2"/>
    <path d="M 200,125 L 200,109 A 36,16 0 0,1 236,125 Z" fill="#EF4444"/>
    <path d="M 200,125 L 236,125 A 36,16 0 0,1 200,141 Z" fill="#3B82F6"/>
    <path d="M 200,125 L 200,141 A 36,16 0 0,1 164,125 Z" fill="#10B981"/>
    <!-- Rolling Pin -->
    <rect x="140" y="145" width="45" height="8" rx="2" fill="#B45309"/>
    <rect x="135" y="147" width="5" height="4" fill="#78350F"/>
    <rect x="185" y="147" width="5" height="4" fill="#78350F"/>
        ''',

        'time_clock': '''
    <!-- Clockmaker Tower & Time -->
    <!-- Clock Tower Body -->
    <rect x="180" y="80" width="40" height="65" rx="4" fill="#0284C7" stroke="#0369A1" stroke-width="2"/>
    <!-- Clock Face -->
    <circle cx="200" cy="102" r="15" fill="#FFFFFF" stroke="#F59E0B" stroke-width="2"/>
    <!-- Clock Hands -->
    <line x1="200" y1="102" x2="200" y2="92" stroke="#0F172A" stroke-width="2" stroke-linecap="round"/>
    <line x1="200" y1="102" x2="208" y2="102" stroke="#0F172A" stroke-width="1.5" stroke-linecap="round"/>
    <!-- Brass Bell on Top -->
    <circle cx="200" cy="75" r="5" fill="#FBBF24"/>
        ''',

        'data_graphs': '''
    <!-- Data Handling & Bar Graph Towers -->
    <!-- 3D Bar Graph Towers -->
    <rect x="155" y="115" width="18" height="30" fill="#38BDF8" stroke="#0284C7" stroke-width="1.5"/>
    <rect x="185" y="95" width="18" height="50" fill="#F59E0B" stroke="#B45309" stroke-width="1.5"/>
    <rect x="215" y="80" width="18" height="65" fill="#10B981" stroke="#047857" stroke-width="1.5"/>
    <!-- Golden Star Flag on Tallest Bar -->
    <line x1="224" y1="80" x2="224" y2="65" stroke="#78350F" stroke-width="2"/>
    <polygon points="224,65 240,71 224,77" fill="#FACC15"/>
        ''',

        'circuits_electric': '''
    <!-- Electricity & Glowing Edison Bulb -->
    <!-- Giant AA Battery -->
    <rect x="145" y="120" width="30" height="22" rx="3" fill="#1E293B" stroke="#0F172A" stroke-width="1.5"/>
    <rect x="175" y="127" width="4" height="8" fill="#F59E0B"/>
    <!-- Glowing Edison Filament Bulb -->
    <circle cx="230" cy="105" r="18" fill="#FEF08A" stroke="#EAB308" stroke-width="2" filter="url(#softGlow)"/>
    <path d="M 226,105 Q 230,95 234,105" stroke="#F97316" stroke-width="2" fill="none"/>
    <rect x="225" y="123" width="10" height="6" fill="#94A3B8"/>
    <!-- Glowing Rays -->
    <line x1="230" y1="80" x2="230" y2="73" stroke="#F59E0B" stroke-width="2"/>
    <line x1="248" y1="88" x2="254" y2="83" stroke="#F59E0B" stroke-width="2"/>
    <line x1="212" y1="88" x2="206" y2="83" stroke="#F59E0B" stroke-width="2"/>
        ''',

        'magnetism': '''
    <!-- Magnetism Horseshoe Magnet -->
    <!-- Horseshoe Magnet -->
    <path d="M 175,135 L 175,105 A 25,25 0 0,1 225,105 L 225,135 L 213,135 L 213,105 A 13,13 0 0,0 187,105 L 187,135 Z" fill="#EF4444" stroke="#B91C1C" stroke-width="2"/>
    <rect x="175" y="123" width="12" height="12" fill="#3B82F6"/>
    <rect x="213" y="123" width="12" height="12" fill="#3B82F6"/>
    <!-- Attracted Paperclips -->
    <ellipse cx="200" cy="142" rx="12" ry="5" stroke="#94A3B8" stroke-width="2" fill="none"/>
        ''',

        'optics_prism': '''
    <!-- Triangular Prism & 7-Color Rainbow -->
    <polygon points="200,90 225,135 175,135" fill="#E0F2FE" opacity="0.85" stroke="#0284C7" stroke-width="2"/>
    <!-- Rainbow Rays Fan -->
    <line x1="215" y1="115" x2="260" y2="95" stroke="#EF4444" stroke-width="2.5"/>
    <line x1="216" y1="117" x2="262" y2="100" stroke="#F97316" stroke-width="2.5"/>
    <line x1="217" y1="119" x2="264" y2="105" stroke="#FACC15" stroke-width="2.5"/>
    <line x1="218" y1="121" x2="266" y2="110" stroke="#22C55E" stroke-width="2.5"/>
    <line x1="219" y1="123" x2="268" y2="115" stroke="#3B82F6" stroke-width="2.5"/>
    <line x1="220" y1="125" x2="270" y2="120" stroke="#8B5CF6" stroke-width="2.5"/>
        ''',

        'chemistry_lab': '''
    <!-- Chemistry Test Tubes & Bubbling Flask -->
    <!-- Wooden Test Tube Rack -->
    <rect x="150" y="125" width="60" height="20" fill="#B45309" stroke="#78350F" stroke-width="2"/>
    <!-- Test Tubes -->
    <rect x="158" y="105" width="8" height="30" rx="4" fill="#A7F3D0" stroke="#059669" stroke-width="1.5"/>
    <rect x="176" y="100" width="8" height="35" rx="4" fill="#FECDD3" stroke="#E11D48" stroke-width="1.5"/>
    <rect x="194" y="108" width="8" height="27" rx="4" fill="#DDD6FE" stroke="#7C3AED" stroke-width="1.5"/>
    <!-- Glass Flask -->
    <polygon points="230,120 245,145 220,145" fill="#BAE6FD" opacity="0.9" stroke="#0284C7" stroke-width="2"/>
    <rect x="229" y="112" width="7" height="10" fill="#BAE6FD" stroke="#0284C7" stroke-width="1.5"/>
    <circle cx="232" cy="108" r="3" fill="#38BDF8"/>
        ''',

        'maps_globe': '''
    <!-- Cartographer Globe & Compass Rose -->
    <!-- Mounted Globe -->
    <circle cx="185" cy="115" r="22" fill="#38BDF8" stroke="#0284C7" stroke-width="2"/>
    <path d="M 170,110 Q 185,100 195,115 Q 185,128 170,110 Z" fill="#22C55E"/>
    <path d="M 185,93 L 185,142" stroke="#B45309" stroke-width="2.5"/>
    <ellipse cx="185" cy="144" rx="14" ry="4" fill="#78350F"/>
    <!-- Compass Rose -->
    <polygon points="245,105 250,120 245,135 240,120" fill="#EF4444"/>
    <polygon points="230,120 245,115 260,120 245,125" fill="#94A3B8"/>
        '''
    }

    # Select graphic or fallback
    graphic_content = theme_graphics.get(theme, theme_graphics['shapes_geometry'])

    svg_end = '''
</svg>'''

    return svg_start + graphic_content + svg_end

def generate_all_thumbnails():
    catalog_path = 'full_games_catalog.json'
    print(f"Reading {catalog_path}...")
    with open(catalog_path, 'r', encoding='utf-8') as f:
        games = json.load(f)

    os.makedirs('images/thumbnails', exist_ok=True)
    generated_svgs = 0

    for game in games:
        gid = game.get('id', '')
        theme = get_theme(game)
        svg_content = build_svg(game, theme)

        svg_path = os.path.join('images', 'thumbnails', f"{gid}.svg")
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        generated_svgs += 1

        # Check if a real AI JPG already exists for this activity
        jpg_path = os.path.join('images', 'thumbnails', f"{gid}.jpg")
        if os.path.exists(jpg_path):
            game['thumb'] = f"images/thumbnails/{gid}.jpg"
        else:
            game['thumb'] = f"images/thumbnails/{gid}.svg"

    print(f"✅ Generated {generated_svgs} SVG 3D diorama thumbnails in images/thumbnails/")

    # Update full_games_catalog.json
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated {catalog_path} with new thumbnail paths")

    # Sync full_games_catalog.js
    js_cat_path = 'full_games_catalog.js'
    js_cat_content = "// Authoritative Games Catalog with Bespoke 3D Diorama Thumbnails\n"
    js_cat_content += "const FULL_GAMES_CATALOG = " + json.dumps(games, indent=2, ensure_ascii=False) + ";\n\n"
    js_cat_content += "if (typeof window !== 'undefined') {\n"
    js_cat_content += "    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n"
    js_cat_content += "    window.GamesCatalog = FULL_GAMES_CATALOG;\n"
    js_cat_content += "}\n"
    js_cat_content += "if (typeof module !== 'undefined' && module.exports) {\n"
    js_cat_content += "    module.exports = { FULL_GAMES_CATALOG };\n"
    js_cat_content += "}\n"
    with open(js_cat_path, 'w', encoding='utf-8') as f:
        f.write(js_cat_content)
    print(f"✅ Synced {js_cat_path}")

if __name__ == '__main__':
    generate_all_thumbnails()
