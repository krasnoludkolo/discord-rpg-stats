import random

from discord.ext import commands
from discord.ext.commands import Context

from controllers.yes_no_controller import YesNoController


class AbstractCog(commands.Cog):

    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command(name='abstrakt')
    async def abstract(self, ctx: Context, n=1):
        print('Recieved command !abstrakt from ' + ctx.author.name + ', processing...')
        result = random.choices(abstracts, k=n)
        await ctx.send("\n".join(result))


abstracts = [
    'Poświęcenie',
    'Rana',
    'Odpowiedzialność',
    'Próba',
    'Strach',
    'Przetrwanie',
    'Pojedynek',
    'Zwierzyna',
    'Bezpieczeństwo',
    'Nadzieja',
    'Dar',
    'Słabość',
    'Pokój',
    'Zdrada',
    'Prawda',
    'Umowa / Zmowa',
    'Przyjaźń',
    'Przesąd',
    'Dzieło',
    'Więzy',
    'Norma',
    'Piękno',
    'Kapłaństwo',
    'Nagroda',
    'Historia',
    'Skrytość',
    'Naiwność',
    'Magia',
    'Ruina',
    'Ciekawość',
    'Wizja',
    'Zabawa',
    'Elita',
    'Ochrona',
    'Muzyka',
    'Szaleństwo',
    'Pogoda',
    'Ekspansja',
    'Rada',
    'Starość',
    'Sekret',
    'Przysięga',
    'Wzór',
    'Rewolucja',
    'Skaza',
    'Okazja',
    'Solidarność',
    'Symbol',
    'Wina',
    'Bestia',
    'Szczodrość',
    'Kłamstwo',
    'Dziedzictwo',
    'Choroba',
    'Porzucenie',
    'Samotność',
    'Żal',
    'Wojna',
    'Natura',
    'Inspiracja',
    'Droga',
    'Wiedza',
    'Niebezpieczeństwo',
    'Chciwość',
    'Ideał',
    'Chwała',
    'Bieda',
    'Zapas',
    'Robota',
    'Bogactwo',
    'Podziemie',
    'Ucieczka',
    'Los',
    'Pamięć',
    'Rywalizacja',
    'Ostrzeżenie',
    'Czas',
    'Zdrowie',
    'Przewaga',
    'Pożoga',
    'Rozkaz',
    'Rodzina',
    'Misja',
    'Pomysł',
    'Dom',
    'Plotka',
    'Ryzyko',
    'Ziemia',
    'Wyobcowanie',
    'Hańba',
    'Władca',
    'Wolność',
    'Duch',
    'Bogowie',
    'Pokusa',
    'Granica',
    'Śmierć',
    'Odnowa',
    'Głupota',
    'Wsparcie'
]
