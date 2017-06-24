from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class RaceIndexPage(Page):
    intro = RichTextField(blank=True)

    class Meta:
        verbose_name = "listado carreras"

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Get all races
        race_pages = self.get_children().live().order_by('-first_published_at')

        context = super(RaceIndexPage, self).get_context(request)
        context['race_pages'] = race_pages
        return context


class RacePageTag(TaggedItemBase):
    content_object = ParentalKey('RacePage', related_name='tagged_items')


class RaceTagIndexPage(Page):

    def get_context(self, request):
        # Get races related to tags
        tag = request.GET.get('tag')
        race_pages = RacePage.objects.filter(tags__name=tag)

        context = super(RaceTagIndexPage, self).get_context(request)
        context['race_pages'] = race_pages

        return context


class RacePage(Page):

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=RacePageTag, blank=True)

    class Meta:
        verbose_name = "carrera"

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information"), FieldPanel('intro'),
        FieldPanel('body', classname="full"),
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
