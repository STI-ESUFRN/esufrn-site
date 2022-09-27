from menu.models import Itens, SubItens, SubSubItens


def menuItens(request):
    itens = Itens.objects.all()
    itenslist = []

    # para cada menu de nível 1
    for item in itens:
        subitens = SubItens.objects.filter(menu=item.id)
        subitenslist = []

        # para cada menu de nível 2
        for subitem in subitens:
            subsubitens = SubSubItens.objects.filter(submenu=subitem)

            subsubitenslist = []
            for subsubitem in subsubitens:
                subsubitenslist.append(subsubitem)

            subitenslist.append(
                {
                    "main": subitem,
                    "subs": subsubitenslist,
                }
            )

        itenslist.append(
            {
                "main": item,
                "subs": subitenslist,
            }
        )

    return {"mainItens": itenslist}
