from pyscript import display, document, window
from pyweb import pydom
from pyweb.pydom import Element

# from out import pydom
# from out.pydom import Element


class Div(Element):
    """Base component builder for an HTML button component.
    __Contains__
    id
    class
    inner_text
    """

    _type = "div"
    _class_list: set = {"uk-container", "container"}

    def __init__(
        self,
        parent: Element,
        id: str = "",
        *,
        class_list: set = {},
        inner_text: str = "",
    ):
        """
        Parameters
        ----------
        id
        class_list
        """
        self._parent: Element = parent
        self._js = document.createElement(self._type)
        self.id: str = id
        cl = self._class_list.union(class_list)
        self.html = f"{inner_text}"
        # -------------------
        # create element
        # ---
        self.__create__()
        # ------------------
        # must be after creation of element
        # ---
        for x in cl:
            self.add_class(x)
        # ------------------

    # -------------------------------------------------------------------------

    def __create__(self):
        self._parent.append(self)