class GPic:
    # Generated Picture
    FLUX = "flux"
    FLUX_REALISM = "flux-realism"
    FLUX_ANIME = "flux-anime"
    FLUX_3D = "flux-3d"
    ANY_DARK = "any-dark"
    TURBO = "turbo"

    CACHE_DIR = "./cache"
    _FILE_COUNTER  = 0

    def __init__(self, prompt, width, height, seed, model=FLUX, nologo=True):
        GPic._FILE_COUNTER += 1
        self.id = GPic._FILE_COUNTER
        self.prompt = prompt
        self.width = width
        self.height = height
        self.seed = seed
        self.model = model
        self.nologo = nologo
        self.init_seed = seed
        self.image = None

    def __repr__(self) -> str:
        return f"{GPic.CACHE_DIR}/{self.get_name()}"

    def get_name(self) -> str:
        return f"prompt{self.id}.png"

    def get_prompt(self) -> dict:
        return {
            "prompt": self.prompt,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "model": self.model,
            "nologo": self.nologo
        }

    def change_variation(self) -> None:
        self.seed += 1

    def reset(self) -> None:
        self.seed = self.init_seed