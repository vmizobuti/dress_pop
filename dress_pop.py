# Implementação conceitual de arte para DressPOP 
#
# Autor: Vinicius Mizobuti / Superlimão
# 
# Versão: 1.0

from make_art import deprecated_make_art
from make_colors import make_colors
from make_sound import sound_parameters
from plot_wave import plot_wave
import inquirer

def query():
    """
    Gets the parameters to generate an art.
    The user will input the art size, a text and a mood
    for design generation.
    """

    # Creates the questions that will be answered by the user
    questions = [
        inquirer.Text('text',
                      message='Escreva o texto que você quer transformar'),
        inquirer.List('size', 
                      message='Escolha o tamanho do seu quadro',
                      choices=['30 x 30', '30 x 40.5', '60 x 81']),
        inquirer.List('scheme', 
                      message='Escolha o esquema de cores',
                      choices=['Vermelhos', 'Verdes', 'Azuis', 'Mix']
                     )
    ]

    # Instantiates the questions
    answers = inquirer.prompt(questions)

    # Parses the answers into their respective parameters
    text = answers['text']
    scheme = answers['scheme']
    width = float(answers['size'].split('x')[0])
    height = float(answers['size'].split('x')[1])

    return text, scheme, width, height

def main():

    # Prompts the user for the art parameters
    input = query()
    data = sound_parameters(input[0])
    plot_wave(data[0], data[1], data[2], data[3], input[0])

    saturation = 0.7
    colors = make_colors(data[3], 5, saturation, input[1])
    deprecated_make_art(colors, input[2], input[3])

if __name__ == '__main__':
    main()