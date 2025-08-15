
import c4d
from c4d import gui, utils

PLUGIN_ID = 1050004

class CityGeneratorDialog(gui.GeDialog):
    def CreateLayout(self):
        self.SetTitle("City Generator - Vincent Ilagan")
        self.SetSize(350, 250)

        self.AddStaticText(1000, c4d.BFH_LEFT, name="Grid Size:")
        self.AddEditNumberArrows(1001, c4d.BFH_SCALEFIT, initw=150)
        self.SetInt32(1001, 10)

        self.AddStaticText(1002, c4d.BFH_LEFT, name="Street Spacing:")
        self.AddEditNumberArrows(1003, c4d.BFH_SCALEFIT, initw=150)
        self.SetInt32(1003, 150)

        self.AddStaticText(1004, c4d.BFH_LEFT, name="Min Height:")
        self.AddEditNumberArrows(1005, c4d.BFH_SCALEFIT, initw=150)
        self.SetInt32(1005, 50)

        self.AddStaticText(1006, c4d.BFH_LEFT, name="Max Height:")
        self.AddEditNumberArrows(1007, c4d.BFH_SCALEFIT, initw=150)
        self.SetInt32(1007, 300)

        self.AddButton(1008, c4d.BFH_CENTER, name="Generate City")
        return True

    def Command(self, id, msg):
        if id == 1008:
            self.GenerateCity()
        return True

    def GenerateCity(self):
        doc = c4d.documents.GetActiveDocument()
        grid_size = self.GetInt32(1001)
        spacing = self.GetInt32(1003)
        min_height = self.GetInt32(1005)
        max_height = self.GetInt32(1007)

        base_cube = c4d.BaseObject(c4d.Ocube)
        base_cube[c4d.PRIM_CUBE_LEN] = c4d.Vector(100, 100, 100)
        base_cube.SetName("Building_Master")

        city_null = c4d.BaseObject(c4d.Onull)
        city_null.SetName("City")
        doc.InsertObject(city_null)

        for x in range(grid_size):
            for z in range(grid_size):
                inst = c4d.BaseObject(c4d.Oinstance)
                inst[c4d.INSTANCEOBJECT_LINK] = base_cube
                height = utils.RangeMap(utils.Random01(), 0, 1, min_height, max_height)
                inst[c4d.PRIM_CUBE_LEN] = c4d.Vector(100, height, 100)
                inst.SetAbsPos(c4d.Vector(x * spacing, height/2, z * spacing))
                doc.InsertObject(inst, parent=city_null)

        c4d.EventAdd()

class CityGeneratorCommand(c4d.plugins.CommandData):
    def Execute(self, doc):
        dlg = CityGeneratorDialog()
        dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE)
        return True

if __name__ == "__main__":
    c4d.plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str="Lightweight City Generator",
        info=0,
        icon=None,
        help="Generate lightweight city with GUI sliders",
        dat=CityGeneratorCommand()
    )
