from typing import List, Literal

from pydantic import BaseModel


class Opera(BaseModel):
    OPERA: Literal[
        "American Airlines",
        "Air Canada",
        "Air France",
        "Aeromexico",
        "Aerolineas Argentinas",
        "Austral",
        "Avianca",
        "Alitalia",
        "British Airways",
        "Copa Air",
        "Delta Air",
        "Gol Trans",
        "Iberia",
        "K.L.M.",
        "Qantas Airways",
        "United Airlines",
        "Grupo LATAM",
        "Sky Airline",
        "Latin American Wings",
        "Plus Ultra Lineas Aereas",
        "JetSmart SPA",
        "Oceanair Linhas Aereas",
        "Lacsa",
    ]


class Mes(BaseModel):
    MES: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


class TipoVuelo(BaseModel):
    TIPOVUELO: Literal["I", "N"]


class Siglades(BaseModel):
    SIGLADES: Literal[
        "Miami",
        "Dallas",
        "Buenos Aires",
        "Toronto",
        "Paris",
        "Ciudad de Mexico",
        "Bogota",
        "Roma",
        "Londres",
        "Ciudad de Panama",
        "Atlanta",
        "Sao Paulo",
        "Rio de Janeiro",
        "Florianapolis",
        "Madrid",
        "Lima",
        "Sydney",
        "Houston",
        "Asuncion",
        "Cataratas Iguacu",
        "Puerto Montt",
        "Punta Arenas",
        "Puerto Natales",
        "Balmaceda",
        "Temuco",
        "Valdivia",
        "Concepcion",
        "La Serena",
        "Copiapo",
        "Calama",
        "Antofagasta",
        "Iquique",
        "Arica",
        "Mendoza",
        "Cordoba",
        "Montevideo",
        "Castro (Chiloe)",
        "Osorno",
        "Orlando",
        "Nueva York",
        "Guayaquil",
        "Cancun",
        "Punta Cana",
        "Los Angeles",
        "Auckland N.Z.",
        "Isla de Pascua",
        "La Paz",
        "Santa Cruz",
        "Curitiba, Bra.",
        "Quito",
        "Bariloche",
        "Rosario",
        "Washington",
        "Tucuman",
        "Melbourne",
        "San Juan, Arg.",
        "Neuquen",
        "Pisco, Peru",
        "Ushuia",
        "Puerto Stanley",
        "Punta del Este",
        "Cochabamba",
    ]


class DiaNom(BaseModel):
    DIANOM: Literal["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Sabado", "Viernes"]


class Features(Opera, Mes, TipoVuelo, Siglades, DiaNom):
    pass


class PayloadFeatures(BaseModel):
    flights: List[Features]


class DelayResponse(BaseModel):
    predict: List[Literal[0, 1]]
