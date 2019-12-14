# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.http import Request

from pudl import items
from pudl.helpers import new_output_dir


class Eia861Spider(scrapy.Spider):
    name = 'eia861'
    allowed_domains = ['www.eia.gov']

    def __init__(self, year=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if year is not None:
            year = int(year)

            if year < 2001:
                raise ValueError("Years before 2001 are not supported")

        self.year = year

    def start_requests(self):
        """Finalize setup and yield the initializing request"""
        # Spider settings are not available during __init__, so finalizing here
        settings_output_dir = self.settings.get("OUTPUT_DIR")
        output_root = os.path.join(settings_output_dir, "eia861")
        self.output_dir = new_output_dir(output_root)

        yield Request("https://www.eia.gov/electricity/data/eia861/")

    def parse(self, response):
        """
        Parse the eia861 home page

        Args:
            response (scrapy.http.Response): Must contain the main page

        Yields:
            appropriate follow-up requests to collect ZIP files
        """
        if self.year is None:
            yield from self.all_forms(response)

        else:
            yield self.form_for_year(response, self.year)

    # Parsers

    def all_forms(self, response):
        """
        Produce requests for collectable Eia861 forms

        Args:
            response (scrapy.http.Response): Must contain the main page

        Yields:
            scrapy.http.Requests for Eia861 ZIP files from 2001 to the most
            recent available
        """
        links = response.xpath(
            "//table[@class='simpletable']"
            "//td[2]"
            "/a[contains(text(), 'ZIP')]")

        for l in links:
            title = l.xpath('@title').extract_first().strip()
            year = int(title.split(" ")[-1])

            if year < 2001:
                continue

            url = response.urljoin(l.xpath("@href").extract_first())

            yield Request(url, meta={"year": year}, callback=self.parse_form)

    def form_for_year(self, response, year):
        """
        Produce request for a specific Eia861 form

        Args:
            response (scrapy.http.Response): Must contain the main page
            year (int): integer year, 2001 to the most recent available

        Returns:
            Single scrapy.http.Request for Eia861 ZIP file
        """
        if year < 2001:
            raise ValueError("Years prior to 2001 not supported")

        path = "//table[@class='simpletable']//td[2]/" \
               "a[contains(@title, '%d')]/@href" % year

        link = response.xpath(path).extract_first()

        if link is not None:
            url = response.urljoin(link)
            return Request(url, meta={"year": year}, callback=self.parse_form)

    def parse_form(self, response):
        """
        Produce the Eia861 form projects

        Args:
            response (scrapy.http.Response): Must contain the downloaded ZIP
                archive

        Yields:
            items.Eia861
        """
        path = os.path.join(
            self.output_dir,
            "eia861-%s.zip" % response.meta["year"])

        yield items.Eia861(
            data=response.body, year=response.meta["year"], save_path=path)
