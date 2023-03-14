# Implementação conceitual de arte para DressPOP 
#
# Autor: Vinicius Mizobuti / Superlimão
# 
# Versão: 1.0

from make_sound import sound_parameters
from make_colors import make_mono, make_grad
from make_rhino import make_rhino
from make_art import make_art
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
                      choices=['30 x 30', '40.5 x 30', '81 x 60']),
        inquirer.List('scheme',
                      message='Escolha o esquema de cores',
                      choices=['Monocromático', 'Gradiente']),
        inquirer.List('colors', 
                      message='Escolha a paleta de cores',
                      choices=['Vermelhos', 'Verdes', 'Azuis', 'Amarelos', 'Mix']
                     )
    ]

    # Instantiates the questions
    answers = inquirer.prompt(questions)

    # Parses the answers into their respective parameters
    text = answers['text']
    scheme = answers['scheme']
    colors = answers['colors']
    width = float(answers['size'].split('x')[0])
    height = float(answers['size'].split('x')[1])

    return text, scheme, colors, width, height

def main():

    # Prompts the user for the art parameters
    input = query()

    # Gets the parameters based on the text input
    data = sound_parameters(input[0])
    
    # Creates the color palette based on user input
    saturation = 0.7
    colors = []
    if input[1] == 'Monocromático':
        colors = make_mono(input[2])
    elif input[1] == 'Gradiente':
        colors = make_grad(data[3], input[2], saturation)
    
    # Creates the vector-based drawings using Rhinoceros
    margins = 3.0
    geo_file = make_rhino(data[3], input[3], input[4], colors, margins)

    # Transforms the Rhinoceros geometry into an Adobe Illustrator file
    art_file = make_art(geo_file, input[3], input[4])

    # Exports the result in a PDF file

    #plot_wave(data[0], data[1], data[2], data[3], input[0])

if __name__ == '__main__':
    main()