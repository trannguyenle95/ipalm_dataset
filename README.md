from model import Properties
from model import Model
model = Model("./model.json")
# Add properties: (name, type)
model.add_prop("mass","continuous")
# Add relations: (parent, child, type, parameters)
model.add_relation("density","linear-gaussian","linear-gaussian","[A:1 B:2 Sigma:3]")