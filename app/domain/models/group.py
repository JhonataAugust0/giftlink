from dataclasses import dataclass

@dataclass
class Group:
    name:         str
    max_value:    float
    draw_status:  bool = False
    id:           int | None = None

    def activate_draw(self):
        if self.draw_status:
            raise ValueError("O sorteio já está ativado.")
        self.draw_status = True

    def deactivate_draw(self):
        self.draw_status = False
