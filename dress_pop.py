# Implementação conceitual de arte para DressPOP 
#
# Autor: Vinicius Mizobuti / Superlimão
# 
# Versão: 1.0

from make_art import make_art
from make_colors import make_colors
import inquirer

def get_art_parameters():
    """
    Gets the parameters to generate an art.
    The user will input the art size, a text and a mood
    for design generation.
    """

    # Creates the questions that will be answered by the user
    questions = [
        inquirer.Text('text',
                      message='Escreva o texto que você quer transformar: '),
        inquirer.List('size', 
                      message='Selecione o tamanho do seu quadro:',
                      choices=['30 x 30', '30 x 40.5', '60 x 81']
                     )
    ]

    # Instantiates the questions
    answers = inquirer.prompt(questions)

    # Parses the answers into their respective parameters
    text = answers['text']
    width = float(answers['size'].split('x')[0])
    height = float(answers['size'].split('x')[1])

    return text, width, height

def main():

    # Prompts the user for the art parameters
    input = get_art_parameters()
    saturation = 0.8
    colors = make_colors(input[0], saturation)
    make_art(colors, input[1], input[2])

if __name__ == '__main__':
    main()