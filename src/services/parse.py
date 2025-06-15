import logging
import re
from typing import Optional

from playwright.async_api import Page, async_playwright


class Parser:
    not_found_msg = "Данные не найдены"

    def __init__(self, page: Page):
        self.data = {}
        self.page = page

    async def parse(self) -> dict[str, str]:
        await self.parse_model_and_mark()
        await self.parse_year()
        await self.parse_price()
        await self.parse_city()
        await self.parse_created_data()
        await self.parse_info_contact()
        await self.parse_technical_specification()

        return self.data

    async def parse_model_and_mark(self) -> None:
        try:
            auto_model_mark = await self.page.locator(
                '//div[@data-ftid="header_breadcrumb"]/div/a'
            ).all()
            self.data["Модель"] = await auto_model_mark[2].inner_text()
            self.data["Марка"] = await auto_model_mark[3].inner_text()
        except Exception as e:
            logging.error(f"Не удалось получить модель и марку машины: {e}")
            self.data["Модель"] = self.not_found_msg
            self.data["Марка"] = self.not_found_msg

    async def parse_year(self) -> None:
        try:
            year_element = await self.page.query_selector("h1")
            year_text = await year_element.inner_text()
            year_match = re.search(r"(?<=, )\d{4}", year_text)
            self.data["Год выпуска"] = year_match.group()
        except Exception as e:
            logging.error(f"Не удалось получить год выпуска: {e}")
            self.data["Год выпуска"] = self.not_found_msg

    async def parse_price(self) -> None:
        try:
            car_price = await self.page.locator(
                '//div[@data-app-root="bull-page"]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[1]'
            ).text_content()
            self.data["Цена"] = car_price.replace("\xa0", " ")
        except Exception as e:
            logging.error(f"Не удалось получить цену: {e}")
            self.data["Цена"] = self.not_found_msg

    async def parse_city(self) -> None:
        try:
            city = str(
                await self.page.locator(
                    '//span[text()="Город"]/parent::div'
                ).text_content(timeout=2000)
            )[7:]
            self.data["Город"] = city
        except Exception as e:
            logging.error(f"Не удалось получить город: {e}")
            self.data["Город"] = self.not_found_msg

    async def parse_created_data(self) -> None:
        try:
            page_created_date = await self.page.locator(
                '//div[@data-ftid="bull-page_bull-views"]/div/div[1]'
            ).text_content()
            page_created_date = re.search(
                r"\d{2}\.\d{2}\.\d{4}", page_created_date
            ).group()
            self.data["Дата создания объявления"] = page_created_date
        except Exception as e:
            logging.error(f"Не удалось получить дату создания объявления: {e}")
            self.data["Дата создания объявления"] = self.not_found_msg

    async def parse_technical_specification(self) -> None:
        try:
            rows = (
                await self.page.get_by_role("table").locator("tr:has(th):has(td)").all()
            )
            for row in rows:
                cells = await row.locator("th, td").all()
                key = await cells[0].inner_text()
                value = await cells[1].inner_text()
                self.data[key] = value.replace("\xa0", " ")
        except Exception as e:
            logging.error(f"Не удалось получить технические характеристики: {e}")
            self.data["Технические характеристики"] = self.not_found_msg

    async def parse_info_contact(self) -> None:
        await self.page.locator('//button[@data-ftid="open-contacts"]').click()
        try:
            await self.page.wait_for_selector(
                '[data-ga-stats-name="phone_number"]', state="visible", timeout=2000
            )
            contact = await self.page.locator(
                '//div[@data-ga-stats-name="phone_number"]/div[@data-ga-stats-track-click="true"]'
            ).inner_text(timeout=1000)
            self.data["Номер телефона"] = contact
            try:
                type_contact = await self.page.locator(
                    '//div[@data-ga-stats-name="phone_number"]/h2'
                ).inner_text(timeout=1000)
                self.data["Тип номера"] = type_contact
            except Exception as ignored:
                logging.warn(f"Не удалось определить тип номера. Ошибка: {ignored}")
                self.data["Тип номера"] = "Постоянный номер"

        except Exception as e:
            logging.error(f"Не удалось определить тип номера и номер. Ошибка: {e}")
            self.data["Номер телефона"] = self.not_found_msg
            self.data["Тип номера"] = self.not_found_msg


class DromService:
    drom_host = "auto.drom.ru"

    async def parse(self, url_page: str) -> Optional[dict[str, str]]:
        if self.drom_host not in url_page:
            raise Exception("Неизвестный домен")

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url_page)
            parser = Parser(page)
            result = await parser.parse()
        return result
