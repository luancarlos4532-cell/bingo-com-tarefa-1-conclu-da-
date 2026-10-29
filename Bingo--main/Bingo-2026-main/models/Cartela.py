import flet as ft
import models.bancoDados
import views.menu as menu
import asyncio
def verificarNumeroPorLetra(numero:int, coordenada:str):
    coluna = coordenada.split(":")[0]
    if(coluna == "0" and numero >= 1 and numero <= 15):
        return False
    elif(coluna == "1" and numero >= 16 and numero <= 30):
        return False
    elif(coluna == "2" and numero >= 31 and numero <= 45):
        return False
    elif(coluna == "3" and numero >= 46 and numero <= 60):
        return False
    elif(coluna == "4" and numero >= 61 and numero <= 75):
        return False
    return True

def mensagemErro(coordenada:str):
    coluna = coordenada.split(":")[0]
    if(coluna == "0"):
        return "Número aceitos: 1-15"
    elif(coluna == "1"):
        return "Número aceitos: 16-30"
    elif(coluna == "2"):
        return "Número aceitos: 31-45"
    elif(coluna == "3"):
        return "Número aceitos: 46-60"
    elif(coluna == "4"):
        return "Número aceitos: 61-75"

# Função do pacote
def verificarValorDigitado(e: ft.Event[ft.TextField]):
    try:
        valor = int(e.control.value)
        coordenada= e.control.data
        if(verificarNumeroPorLetra(valor,coordenada)):
            e.control.label = mensagemErro(coordenada)
            e.control.border_color = ft.Colors.RED
        else:
            e.control.label = None
            e.control.border_color = ft.Colors.GREEN
    except:
        e.control.label = "Somente números"
        e.control.border_color = ft.Colors.RED

    e.page.update()

def verificarValorValido(valor, coordenada):
    try:
        valor = int(valor)
        if(verificarNumeroPorLetra(valor,coordenada)):
            return False
        else:
            return True
    except:
        return False

def verificaEAlertaSeTemCamposComValoresDuplicados(listaColunas):
    possuiValoresDuplicados = False
    for coluna in listaColunas:
            tamanhoLista = len(coluna.controls)
            contador = 0
            while contador < tamanhoLista:
                contadorComparador = contador + 1
                while contadorComparador < tamanhoLista:
                    if isinstance(coluna.controls[contador], ft.TextField) and isinstance(coluna.controls[contadorComparador], ft.TextField) and coluna.controls[contador].value != "":
                        if(coluna.controls[contador].value == coluna.controls[contadorComparador].value):
                            coluna.controls[contadorComparador].border_color = ft.Colors.RED
                            coluna.controls[contadorComparador].label = "Valor Duplicado"
                            possuiValoresDuplicados = True
                    contadorComparador+=1
                contador+=1
    return possuiValoresDuplicados

def verificaEAlertaSeTemCamposVazios(listaColunas):
        possuiVazios = False
        for coluna in listaColunas:
            for item in coluna.controls:
                if(isinstance(item, ft.TextField)):
                    if(item.value == None or item.value == ""):
                        possuiVazios = True
                        item.border_color = ft.Colors.YELLOW
                        item.label = "Não pode ficar vazio"
        return possuiVazios

# Função do pacote
def limparCamposCartela(listaColunas,campoCodigo,):   
    campoCodigo.value = ""
    campoCodigo.label = "Código Cartela"
    campoCodigo.border_color = ft.Colors.WHITE
    for coluna in listaColunas:
        for item in coluna.controls:
            if(isinstance(item, ft.TextField)):
                item.value = ""
                item.label = item.data
                item.border_color = ft.Colors.WHITE
                  
async def limpartextomensagem(textoMensagem,page):
    await asyncio.sleep(4)
    textoMensagem.value=""
    page.update()
def cadastrarCartela(e: ft.Event[ft.Button]):
    listaColunas = e.control.data[0]
    campoCodigo = e.control.data[1].content.content
    codigo = campoCodigo.value.strip()
    codigoValido = codigo.strip() != ""
    codigoduplicado = (codigoValido and models.bancoDados.encontrar_cartela((codigo)) is not None)
    textoMensagem = e.control.data[2]

    listaB = []
    listaI = []
    listaN = []
    listaG = []
    listaO = []

    contadorCorretos = 0
    contadorColunas = 0

    for coluna in listaColunas:
        for item in coluna.controls:
            if(item.data != None and verificarValorValido(item.value, item.data)):
                if(contadorColunas == 0):
                    listaB.append(item.value)
                elif(contadorColunas == 1):
                    listaI.append(item.value)
                elif(contadorColunas == 2):
                    listaN.append(item.value)
                elif(contadorColunas == 3):
                    listaG.append(item.value)
                elif(contadorColunas == 4):
                    listaO.append(item.value)
                contadorCorretos += 1
        contadorColunas += 1

    possuiValoresDuplicados = verificaEAlertaSeTemCamposComValoresDuplicados(listaColunas)
    possuiCamposVazios = verificaEAlertaSeTemCamposVazios(listaColunas)

    if(not codigoValido):
        campoCodigo.border_color = ft.Colors.YELLOW
        campoCodigo.label = "Não pode ficar vazio"
    elif codigoduplicado:
        campoCodigo.border_color = ft.Colors.RED
        campoCodigo.label = "Código já cadastrado"

    else:
        campoCodigo.border_color = ft.Colors.GREEN
        campoCodigo.label = ""

    #criar Verificação se o código ja esta cadastrado

    if(contadorCorretos == 24 and codigoValido and not possuiValoresDuplicados and not possuiCamposVazios and not codigoduplicado):
        models.bancoDados.adicionarCartela(codigo.strip().upper(),listaB,listaI,listaN,listaG,listaO)
        textoMensagem.color = ft.Colors.GREEN
        textoMensagem.value = f"Cartela {codigo} cadastrado com sucesso"
        #limpar campos
        e.page.run_task(limpartextomensagem,textoMensagem,e.page)
        limparCamposCartela(listaColunas,campoCodigo,)
    if(contadorCorretos != 24 or not codigoValido or possuiValoresDuplicados or possuiCamposVazios or codigoduplicado):
        textoMensagem.color = ft.Colors.RED
        textoMensagem.value = f"Erro ao cadastrar a cartela {codigo}"
        e.page.run_task(limpartextomensagem,textoMensagem,e.page)
    if(codigoduplicado):
        textoMensagem.color = ft.Colors.RED
        textoMensagem.value = f"Erro ao cadastrar a cartela {codigo}, código já cadastrado"
        e.page.run_task(limpartextomensagem,textoMensagem,e.page)
    e.page.update()

def verificarSeCodigoJaCadastrado(e: ft.Event[ft.TextField]):
        codigo = e.control.value.strip()
        if codigo == "":
            e.control.border_color = ft.Colors.WHITE
            e.control.label = "Codigo Cartela"
        elif models.bancoDados.encontrar_cartela(codigo) is not None:
            e.control.border_color = ft.Colors.RED
            e.control.label = "Código já cadastrado"
        else:
            e.control.border_color = ft.Colors.GREEN
            e.control.label = "Codigo disponível"
        e.page.update()
def pegarListaCartelas():
    return models.bancoDados.pegarListaCartelas()

def excluirCartela(e: ft.Event[ft.Button]):
    indiceEncontrado = e.control.data[0]
    estruturaPagina = e.control.data[1]

    models.bancoDados.removerCartela(indiceEncontrado)
    e.page.pop_dialog()

    menu.ao_mudar_aba(estruturaPagina, 2)

def fecharDialogo(e: ft.Event[ft.Button]):
    e.page.pop_dialog()
    e.page.update()

def verificarCondicoesDeExclusao(e: ft.Event[ft.Button]):
    codigoCartela = e.control.data[0]
    dialogo = e.control.data[1]
    estruturaPagina = e.control.data[2]

    indiceEncontrado = models.bancoDados.encontrar_cartela(codigoCartela)
    if indiceEncontrado == None :
        dialogo.content.value = "Erro: Não foi possivel encontrar a cartela"
        e.page.show_dialog(dialogo)
    else:
        dialogo.content.value = f"Tem certeza que deseja excluir a cartela com Código: {codigoCartela}"
        dialogo.actions = [ft.Button("Cancelar", on_click=fecharDialogo),
                           ft.Button("Excluir", on_click=excluirCartela ,data=[indiceEncontrado, estruturaPagina] )]
        e.page.show_dialog(dialogo)
    e.page.update()
