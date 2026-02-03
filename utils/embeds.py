import discord
from discord import Embed

class Embeds:
    @staticmethod
    def create_embed(title, description, color):
        return Embed(title=title, description=description, color=color)
    
    @staticmethod
    def create_error_embed(description):
        return Embed(title="Error", description=description, color=discord.Color.red())
    
    @staticmethod
    def create_success_embed(title, description):
        return Embed(title=title, description=description, color=discord.Color.green())
    
    @staticmethod
    def create_warning_embed(title, description):
        return Embed(title=title, description=description, color=discord.Color.orange())
    
    @staticmethod
    def create_info_embed(title, description=None):
        return Embed(title=title, description=description, color=discord.Color.blue())