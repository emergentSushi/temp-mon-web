from pydantic import BaseModel


class SensorConfig(BaseModel):
    mac: str
    name: str
    graph_colour: str


PATH_TO_SQLITE = "data/grid_data.db"

sensors: dict[str, SensorConfig] = {
    "A4:C1:38:3B:86:DE": SensorConfig(mac="A4:C1:38:3B:86:DE", name="Larder", graph_colour="rgb(255, 99, 132)"),
    "A4:C1:38:73:28:DC": SensorConfig(mac="A4:C1:38:73:28:DC", name="Office", graph_colour="rgb(255, 159, 64)"),
    "A4:C1:38:A4:86:79": SensorConfig(mac="A4:C1:38:A4:86:79", name="Roof", graph_colour="rgb(75, 192, 192)"),
    "A4:C1:38:56:5C:07": SensorConfig(mac="A4:C1:38:56:5C:07", name="Kitchen", graph_colour="rgb(54, 162, 235)"),
    "A4:C1:38:EE:06:4C": SensorConfig(mac="A4:C1:38:EE:06:4C", name="Outdoor", graph_colour="rgb(97, 255, 51)"),
}
