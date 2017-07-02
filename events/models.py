from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from djmoney.models.fields import MoneyField


class RaceIndexPage(Page):
    intro = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', verbose_name="Imagen Principal", on_delete=models.SET_NULL, related_name='+',
        blank=True, null=True,
    )

    class Meta:
        verbose_name = "listado carreras"

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('image'),
    ]

    def get_context(self, request):
        # Get all races
        race_pages = reversed(self.get_children().live().order_by('racepage'))

        context = super(RaceIndexPage, self).get_context(request)
        context['race_pages'] = race_pages
        return context


class RacePageTag(TaggedItemBase):
    content_object = ParentalKey('RacePage', related_name='tagged_items')


class RaceTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get('tag')
        race_pages = RacePage.objects.filter(tags__name=tag)

        context = super(RaceTagIndexPage, self).get_context(request)
        context['race_pages'] = race_pages

        return context


class RacePage(Page):
    is_international = models.BooleanField(verbose_name="Internacional")
    distance = models.IntegerField(verbose_name="Distancia (Km)")
    cost = MoneyField(
        verbose_name="Costo",
        max_digits=10,
        decimal_places=3,
        default_currency='DOP',
        currency_choices=(('USD', 'USD $'), ('DOP', 'DOP $')),
        null=True,
        blank=True,
    )
    city = models.ForeignKey("cities_light.City", null=True, on_delete=models.SET_NULL)
    route_description = models.TextField(verbose_name="Detalles de ruta", blank=True)
    date = models.DateTimeField(verbose_name="Fecha")
    sign_in = RichTextField(verbose_name="Detalles de inscripcción", blank=True)
    notes = RichTextField(verbose_name="Informacion adicional", blank=True)
    tags = ClusterTaggableManager(through=RacePageTag, blank=True)

    class Meta:
        verbose_name = "carrera"

    parent_page_types = [
        RaceIndexPage,
    ]
    search_fields = Page.search_fields + [
        index.SearchField('distance'),
        index.SearchField('city'),
        index.SearchField('date'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('is_international'),
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('cost'),
            FieldPanel('city'),
            FieldPanel('route_description'),
            FieldPanel('sign_in'),
            FieldPanel('distance'),

        ], heading="Informacion"),
        FieldPanel('notes', classname="full"),
        InlinePanel('gallery_images', label="Imagenes"),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


class RacePageGalleryImage(Orderable):
    page = ParentalKey(RacePage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


# Define page creation Rules
RaceIndexPage.subpage_types = [RacePage]
RacePage.subpage_types = []
