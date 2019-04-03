uint8 BAY_ROCKET_BOT_LEFT  = 0
uint8 BAY_ROCKET_BOT_RIGHT = 1
uint8 BAY_ROCKET_MID_LEFT  = 2
uint8 BAY_ROCKET_MID_RIGHT = 3
uint8 BAY_ROCKET_TOP_LEFT  = 4
uint8 BAY_ROCKET_TOP_RIGHT = 5

uint8 BAY_CARGO_SHIP_FAR_LEFT    = 0
uint8 BAY_CARGO_SHIP_MID_LEFT    = 1
uint8 BAY_CARGO_SHIP_NEAR_LEFT   = 2
uint8 BAY_CARGO_SHIP_FRONT_LEFT  = 3
uint8 BAY_CARGO_SHIP_FRONT_RIGHT = 4
uint8 BAY_CARGO_SHIP_NEAR_RIGHT  = 5
uint8 BAY_CARGO_SHIP_MID_RIGHT   = 6
uint8 BAY_CARGO_SHIP_FAR_RIGHT   = 7

Header    header
float32   left_hp_cargo_confidence
float32   left_hp_hatch_panel_confidence
float32   right_hp_cargo_confidence
float32   right_hp_hatch_panel_confidence
float32[] left_rocket_cargo_confidence
float32[] left_rocket_hatch_panel_confidence
float32[] right_rocket_cargo_confidence
float32[] right_rocket_hatch_panel_confidence
float32[] cargo_ship_cargo_confidence
float32[] cargo_ship_hatch_panel_confidence
