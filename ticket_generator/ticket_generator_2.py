import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


class TicketGenerator:
    def __init__(self, transport_number, cost):
        self.cost = cost
        self.transport_number = transport_number.upper()
        self.path = fr".\ticket_generator"
        self.ticket = Image.open(fr"{self.path}\second_version_ticket.jpg")
        self.new_ticket = Image.new("RGB", self.ticket.size, (255, 255, 255))
        self.font = ImageFont.truetype("arial.ttf", 19)
        self.months = {"1": "января",
                       "2": "февраля",
                       "3": "марта",
                       "4": "апреля",
                       "5": "мая",
                       "6": "июня",
                       "7": "июля",
                       "8": "августа",
                       "9": "сентября",
                       "10": "октября",
                       "11": "ноября",
                       "12": "декабря"
                       }
        self.custom_font = ImageFont.truetype(fr"{self.path}\tickets\font\smartphone_time_font.ttf", 21)
        self.font_for_transport = ImageFont.truetype(fr"{self.path}\tickets\font\Muli-ExtraBold.ttf", 24)

    def add_placeholders(self):
        # paste pic to new ticket
        self.new_ticket.paste(self.ticket, (0, 0))

        # create mask(remove) and draw it
        mask = Image.new("L", self.new_ticket.size, 255)
        mask_draw = ImageDraw.Draw(mask)

        # mask for number
        mask_draw.rectangle((3, 396, 588, 427), fill=0)

        # mask for time and date
        mask_draw.rectangle((5, 488, 586, 593), fill=0)

        # mask for swipe button
        mask_draw.rectangle((0, 1242, 591, 1280), fill=0)

        # mask for smartphone time
        mask_draw.rectangle((48, 23, 113, 46), fill=0)

        self.new_ticket.putalpha(mask)

        # draw white rect
        draw = ImageDraw.Draw(self.new_ticket)

        # white rect for number
        draw.rectangle((3, 396, 588, 475), fill=(255, 255, 255))

        # white rect for time and date
        draw.rectangle((5, 488, 586, 593), fill=(255, 255, 255))

        # white rect for swipe button
        draw.rectangle((0, 1242, 591, 1280), fill=(255, 255, 255))

        # white rect for smartphone time
        draw.rectangle((48, 23, 113, 46), fill=(255, 255, 255))

    def get_time(self):
        # get time
        d_and_t = datetime.today()
        date = f"{d_and_t.day} {self.months[str(d_and_t.month)]} {d_and_t.year} "
        time = str(d_and_t.hour) + ":"
        minutes = str(d_and_t.minute) if len(str(d_and_t.minute)) == 2 else "0"+str(d_and_t.minute)
        time += minutes
        return date, time

    def modify_ticket(self):
        self.add_placeholders()
        date_and_time = self.get_time()
        text_write = ImageDraw.Draw(self.new_ticket)
        text_write.text((242, 420), self.transport_number, font=self.font_for_transport, fill=(0, 0, 0))
        text_write.text((190, 531), "".join(date_and_time), font=ImageFont.truetype("arial.ttf", 24), fill=(0, 0, 0))
        text_write.text((231, 563),f"Сумма {self.cost} ₸", font=ImageFont.truetype("arial.ttf", 24), fill=(0, 0, 0))
        text_write.text((52, 20), date_and_time[1], font=self.custom_font, fill=(0, 0, 0))
        self.get_ticket()

    def get_ticket(self):
        self.new_ticket = self.new_ticket.convert("RGB")
        self.new_ticket.save(fr"{self.path}\tickets\{self.transport_number}.jpg", quality=100)
        
