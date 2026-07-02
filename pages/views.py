from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse

from .forms import QuoteForm
from .models import BlogPost, Service, SiteSettings
from .services import notify_quote_request
from .utils.block_render import get_block_text

BLOG_POSTS_PER_PAGE = 3


def _page_meta(page: str, defaults: dict[str, str]) -> dict[str, str]:
    return {
        'meta_title': get_block_text(page, 'meta_title', fallback=defaults['meta_title']),
        'meta_description': get_block_text(
            page,
            'meta_description',
            fallback=defaults['meta_description'],
        ),
    }


def _blog_page(request):
    paginator = Paginator(
        BlogPost.objects.filter(is_published=True),
        BLOG_POSTS_PER_PAGE,
    )
    page_number = request.GET.get('page', 1)

    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def home(request):
    return render(request, 'pages/home.html', _page_meta('home', {
        'meta_title': 'Professional Welding Services in Poole',
        'meta_description': (
            'Certified welding, metal structures, and fabrication for demanding '
            'industrial projects. Request a quote from KHODAK Metal Solution.'
        ),
    }))


def about(request):
    return render(request, 'pages/about.html', _page_meta('about', {
        'meta_title': 'About Us — Engineering Integrity Since 2014',
        'meta_description': (
            'KHODAK Metal Solution delivers structural excellence across critical '
            'industrial sectors. Precision engineering, certified safety, premium craftsmanship.'
        ),
    }))


def services_list(request):
    return render(request, 'pages/services.html', _page_meta('services', {
        'meta_title': 'Welding & Fabrication Services',
        'meta_description': (
            'Precision engineering and heavy-duty execution. Welding, structure '
            'installation, manufacturing, TIG, electrode welding, and metal repair.'
        ),
    }))


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_published=True)
    return render(request, 'pages/service_detail.html', {
        'service': service,
        'meta_title': f'{service.title} — Professional Metal Fabrication',
        'meta_description': service.short,
    })


def portfolio(request):
    return render(request, 'pages/portfolio.html', _page_meta('portfolio', {
        'meta_title': 'Our Work — Engineering Portfolio',
        'meta_description': (
            'A showcase of structural integrity and precision engineering. '
            'Explore industrial, commercial, and residential metal fabrication projects.'
        ),
    }))


def blog_list(request):
    page_obj = _blog_page(request)
    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        **_page_meta('blog', {
            'meta_title': 'Engineering Insights & Welding Technologies',
            'meta_description': (
                'Expert guides on structural integrity, precision welding techniques, '
                'and industrial fabrication standards from the KHODAK engineering team.'
            ),
        }),
    }

    if request.htmx:
        return render(request, 'partials/blog_grid.html', context)

    return render(request, 'pages/blog.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:2]
    return render(request, 'pages/blog_detail.html', {
        'post': post,
        'related_posts': related,
        'meta_title': post.title,
        'meta_description': post.excerpt,
    })


def faq(request):
    return render(request, 'pages/faq.html', _page_meta('faq', {
        'meta_title': 'Frequently Asked Questions',
        'meta_description': (
            'Answers to common questions about welding certifications, project types, '
            'response times, and service areas from KHODAK Metal Solution.'
        ),
    }))


def contact(request):
    return render(request, 'pages/contact.html', _page_meta('contact', {
        'meta_title': 'Contact — Request a Quote',
        'meta_description': (
            'Get in touch with KHODAK Metal Solution. Submit project specifications '
            'or call our Poole workshop for professional welding services.'
        ),
    }))


def quote_submit(request):
    if request.method != 'POST':
        return redirect('contact')

    id_prefix = request.POST.get('id_prefix', 'quote')
    compact = request.POST.get('compact') == '1'

    form = QuoteForm(request.POST, id_prefix=id_prefix, compact=compact)

    if form.is_valid():
        quote = form.save(commit=False)
        quote.privacy_accepted = True
        quote.save()
        notify_quote_request(quote)

        if request.htmx:
            return render(request, 'partials/quote_success.html', {
                'compact': compact,
            })

        return redirect('thank_you')

    context = {
        'form': form,
        'compact': compact,
        'id_prefix': id_prefix,
        'selected_service': request.POST.get('service', ''),
    }

    if request.htmx:
        return render(request, 'partials/quote_form.html', context, status=422)

    return render(request, 'pages/contact.html', {
        **_page_meta('contact', {
            'meta_title': 'Contact — Request a Quote',
            'meta_description': (
                'Get in touch with KHODAK Metal Solution. Submit project specifications '
                'or call our Poole workshop for professional welding services.'
            ),
        }),
        'quote_form': form,
    })


def thank_you(request):
    return render(request, 'pages/thank_you.html', {
        'meta_title': 'Thank You',
        'meta_description': 'Your enquiry has been received. We will contact you shortly.',
        'noindex': True,
    })


def privacy(request):
    return render(request, 'pages/privacy.html', _page_meta('privacy', {
        'meta_title': 'Privacy Policy',
        'meta_description': (
            'How KHODAK Metal Solution collects, uses, and protects your personal data '
            'under UK GDPR when you use our website or submit an enquiry.'
        ),
    }))


def terms(request):
    return render(request, 'pages/terms.html', _page_meta('terms', {
        'meta_title': 'Terms of Service',
        'meta_description': (
            'Terms of service for using the KHODAK Metal Solution website and engaging '
            'our welding, fabrication, and installation services in the UK.'
        ),
    }))


def robots_txt(request):
    site = SiteSettings.load()
    return TemplateResponse(
        request,
        'robots.txt',
        {'site_url': site.site_url},
        content_type='text/plain',
    )


def sitemap_xml(request):
    site = SiteSettings.load()
    pages = [
        {'loc': '/', 'priority': '1.0'},
        {'loc': '/about/', 'priority': '0.8'},
        {'loc': '/services/', 'priority': '0.8'},
        {'loc': '/portfolio/', 'priority': '0.8'},
        {'loc': '/blog/', 'priority': '0.7'},
        {'loc': '/faq/', 'priority': '0.7'},
        {'loc': '/contact/', 'priority': '0.8'},
        {'loc': '/privacy/', 'priority': '0.3'},
        {'loc': '/terms/', 'priority': '0.3'},
    ]
    for svc in Service.objects.filter(is_published=True):
        pages.append({'loc': f'/services/{svc.slug}/', 'priority': '0.7'})
    for post in BlogPost.objects.filter(is_published=True):
        pages.append({'loc': f'/blog/{post.slug}/', 'priority': '0.6'})
    return TemplateResponse(
        request,
        'sitemap.xml',
        {'pages': pages, 'site_url': site.site_url},
        content_type='application/xml',
    )
