import image_manager as image_manager
import sys
import pygame
import tkinter as tk

class CapturedPiecesDisplay:
    def __init__ (self,player):
        self.player = player
        self.image_manager = image_manager.ImageManager()

    def draw_board(self):
        if self.player.color ==  "WHITE":
            #Posição inicial do display de peças capturadas do jogador branco
            print("")
        else:
            #posicao inicial do display de peças capturadas do jogador preto
            print("")

    def possible_moves(self):
        #retorna os movimentos possíveis de uma peça quando a mesma esta dentro do tabuleiro de peças capturadas
        pass

    def handle_select_piece(self):
        #seleciona uma peça capturada
        pass