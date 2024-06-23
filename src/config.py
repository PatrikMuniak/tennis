import yaml

venue_config=None


class Venue_Config:
    def __init__(self, path) -> None:
        self.path = path
        self.cfg_dict = self.load_config()

    def load_config(self):
        with open('config.yaml', 'r') as file:
            venue_config = yaml.safe_load(file)
        return venue_config
    
    def retrieve_params(self, *args):
        out = []
        for venue in self.cfg_dict.get("venue_list",[]):
            row = {}
            for arg in args:
                row[arg]=venue.get(arg, None)

            out.append(row)

            
        return out

    def get_by_id(self, key, *args):
        for venue in self.cfg_dict.get("venue_list",[]):
            if key == venue["venue_id"]:
                row = {}
                for arg in args:
                    row[arg]=venue.get(arg, None)

                return row

            
        return -1


venues_cfg = Venue_Config("config.yaml")
venue_config = venues_cfg.cfg_dict