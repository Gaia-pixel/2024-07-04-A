import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self.formaSelezionata = None
        self.annoSelezionato = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDD(self):
        anni = self._model.get_years()
        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(key = a, data = a, on_click = self.handleDD))
        self._view.update_page()

    def handleDD(self, e):
        self.annoSelezionato = e.control.data
        forme = self._model.get_shapes(self.annoSelezionato)
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))
        self._view.update_page()


    def handle_graph(self, e):
        self.formaSelezionata = self._view.ddshape.value
        if self.formaSelezionata is None:
            self._view.txt_result1.controls.append(ft.Text("Selezionare una forma"))
            self._view.update_page()
            return
        self._model.buildGraph(self.annoSelezionato, self.formaSelezionata)
        n, a = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"grafo creato con {n} nodi e {a} archi"))
        self._view.update_page()



    def handle_path(self, e):
        pass
