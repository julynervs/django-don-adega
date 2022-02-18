# filtro que define dados incorretos como None
def valor_correto_ou_nada(chave):
    if conta_bling[chave] == '':
        logging.warning(f"____{chave} da conta {n} incorreta ou não existente, None definido no campo")
        return None
    else:
        logging.info(f"____{chave} da conta {n} cadastrada")
        return conta_bling[chave]

# filtro para existencia de um dado no JSON do Bling
def chave_existe(chave_bling):
    if chave_bling in conta_bling.keys():
        return True
    else:
        return False
