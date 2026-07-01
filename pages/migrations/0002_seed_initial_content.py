from datetime import date

from django.db import migrations


def seed_content(apps, schema_editor):
    SiteSettings = apps.get_model('pages', 'SiteSettings')
    Service = apps.get_model('pages', 'Service')
    PortfolioItem = apps.get_model('pages', 'PortfolioItem')
    BlogPost = apps.get_model('pages', 'BlogPost')
    FAQItem = apps.get_model('pages', 'FAQItem')

    if Service.objects.exists():
        return

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'KHODAK Metal Solution',
            'site_short': 'KHODAK',
            'site_tagline': 'Built for Durability. Engineered with Precision.',
            'site_description': (
                'Certified welding, metal structures, and fabrication for demanding '
                'industrial projects in Poole and across the UK.'
            ),
            'site_url': 'https://khodakmetal.co.uk',
            'site_phone': '+44 1202 000 000',
            'site_email': 'info@khodakmetal.co.uk',
            'site_address': 'Industrial Estate, Poole, Dorset BH15, UK',
            'site_year': 2024,
        },
    )

    services = [
        ('welding-works', 'SVC-01', 'Welding Works', 'Professional arc and fusion welding for industrial-grade joints.', 'robot', 1),
        ('structure-installation', 'SVC-02', 'Structure Installation', 'On-site assembly and erection of heavy steel frameworks.', 'wrench', 2),
        ('structure-manufacturing', 'SVC-03', 'Structure Manufacturing', 'Custom fabrication from blueprint to finished assembly.', 'factory', 3),
        ('tig-welding', 'SVC-04', 'TIG Welding', 'Precision GTAW for stainless steel, aluminium, and alloys.', 'flame', 4),
        ('electrode-welding', 'SVC-05', 'Electrode Welding', 'SMAW for carbon steel structures and heavy-duty repairs.', 'bolt', 5),
        ('metal-repair', 'SVC-06', 'Metal Product Repair', 'Structural reinforcement and restoration of worn components.', 'repair', 6),
    ]
    for slug, code, title, short, icon, order in services:
        Service.objects.create(
            slug=slug,
            code=code,
            title=title,
            short=short,
            icon=icon,
            sort_order=order,
        )

    portfolio = [
        ('omega-metalworks', 'industrial', 'Omega Metalworks Facility', 'Detroit, MI', '24,000 SQ FT', 'project-frame.png', 1),
        ('nexus-tower', 'commercial', 'Nexus Corporate Tower', 'Chicago, IL', '12 STORIES', 'project-frame.png', 2),
        ('bridge-reinforcement', 'repairs', 'Bridge Support Reinforcement', 'Pittsburgh, PA', 'STRUCTURAL WELDING', 'welder.png', 3),
        ('ironwood-residence', 'residential', 'Ironwood Residence', 'Austin, TX', 'CUSTOM FABRICATION', 'workshop.png', 4),
    ]
    for slug, category, title, location, detail, image, order in portfolio:
        PortfolioItem.objects.create(
            slug=slug,
            category=category,
            title=title,
            location=location,
            detail=detail,
            static_image=image,
            sort_order=order,
        )

    posts = [
        ('future-heavy-duty-structural-installation', 'technology', 'The Future of Heavy-Duty Structural Installation',
         'Next-generation crane operations and automated alignment systems are reshaping how we erect industrial frameworks.',
         date(2024, 10, 24), True, 'project-frame.png'),
        ('tig-vs-mig-aluminum', 'materials', 'TIG vs. MIG: Choosing the Right Weld for Aluminum Projects',
         'A technical comparison of GTAW and GMAW for aerospace-grade aluminium assemblies under high-stress conditions.',
         date(2024, 6, 15), False, 'tig-weld.png'),
        ('reading-blueprints-precision', 'technology', 'Reading Blueprints: Precision Standards in Industrial Fabrication',
         'How engineering teams translate CAD drawings into measurable tolerances on the shop floor.',
         date(2024, 9, 10), False, 'blueprints.png'),
        ('aws-safety-standards', 'safety', 'Safety First: AWS Standards in Modern Metal Fabrication',
         'Essential protocols for weld quality assurance and operator protection on demanding job sites.',
         date(2024, 8, 5), False, 'welder.png'),
    ]
    for slug, category, title, excerpt, published_at, featured, image in posts:
        BlogPost.objects.create(
            slug=slug,
            category=category,
            title=title,
            excerpt=excerpt,
            published_at=published_at,
            is_featured=featured,
            static_image=image,
        )

    faqs = [
        ('What welding certifications do your team hold?',
         'Our welders are certified to AWS D1.1 structural welding standards and hold coded qualifications for TIG, MIG, and electrode processes. We maintain ISO 9001 quality management compliance across all projects.'),
        ('Do you work on residential and commercial projects?',
         'Yes. We handle industrial frameworks, commercial fit-outs, and residential structural steel — from custom staircases to full building erection. Project scope determines the crew and equipment deployed.'),
        ('How quickly can you respond to an urgent repair?',
         'For emergency structural repairs in the Poole and Dorset area, we typically mobilise within 24 hours. Contact us directly for same-day assessment on critical failures.'),
        ('Can I submit blueprints or CAD files with my enquiry?',
         'Absolutely. Upload PDF, DWG, or image files up to 5 MB through our contact form. Our engineering team reviews specifications before providing a detailed quote.'),
        ('What areas do you serve?',
         'Our workshop is based in Poole, Dorset. We serve clients across the South West, London, and nationwide for large-scale industrial contracts.'),
    ]
    for index, (question, answer) in enumerate(faqs, start=1):
        FAQItem.objects.create(question=question, answer=answer, sort_order=index)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]
