from pydantic import SecretStr

from appkit_commons.configuration.base import BaseConfig


class ImageGeneratorConfig(BaseConfig):
    google_api_key: SecretStr
    """required for Google image models (Imagen3, Imagen4)"""
    blackforestlabs_api_key: SecretStr
    """required for Black Forest Labs Flux models"""
    openai_api_key: SecretStr
    """required for OpenAI images models (GPT-Image-1)"""
    openai_base_url: str | None = None
    """optional, for OpenAI-compatible endpoints, e.g. Azure OpenAI"""
    tmp_dir: str = "./uploaded_files"
    """temp directory for storing generated images, default Reflex.dev upload dir"""


prompt_list = [
    # 1. Aqua-haariges Anime-Mädchen
    "Erwachsenes Anime-Mädchen, langes aqua-glasiges Haar und Augen, einzelner linker Pferdeschwanz, hellgrünes traditionelles Kleid, hyperdetailliert, scharfer Fokus",  # noqa: E501
    # 3. Japanische Tengu-Fantasy-Render
    "Japanischer Tengu-Drache, dramatische stimmungsvolle Beleuchtung, filmische Atmosphäre, hohe Auflösung",  # noqa: E501
    # 4. Brüllender Löwenkönig
    "Mächtiger brüllender Löwe, mit einer Krone auf",
    # 9. Biolumineszierender Wal im Canyon
    "Enormer Wal, der durch den Antelope Canyon in glühendem biolumineszentem Wasser gleitet",  # noqa: E501
    # 10. Cartoon-Tiger mit Fächer
    "Cartoon-Tiger, der mit einem Blattfächer wedelt, Herbstblätter auf dem Boden, prägnante Linien, filmische Beleuchtung, ultra-detaillierte Umgebung",  # noqa: E501
    # 11. Klassisches Porträt im Öl-Stil
    "Porträt eines stoischen Gentleman, symmetrische Komposition, ruhiger Blick, malerische Details",  # noqa: E501
    # 12. Illustration eines Malerstudios
    "Innenillustration eines Künstlerateliers, weiche Herbstpalette, Gouache-Textur",
    # 13. Futuristische Stadtlandschaft 2100
    "Große Stadtlandschaft im Jahr 2100, atmosphärisch hyperrealistisch 16K, epische Komposition, filmische Beleuchtung",  # noqa: E501
    # 14. Fantasy-Insel-Portal
    "Fantasy-Insel mit volumetrischem magischem Portal, Figur in Wolken, Regenbogenlicht, Mittelschnitt, High-Detail-Stil",  # noqa: E501
    # 15. Feldbaum-Matte-Malerei
    "Einsamer volumiöser Baum im Sommer auf offenem Feld, Plein-Air-Stil, detailliert, realistisch",  # noqa: E501
    # 16. Futuristische Flugzeug-Kinematik
    "Kinematisches Konzept: futuristisches Flugzeug, das durch eine Neon-Stadtstraße fliegt, Tiefenschärfe-Unschärfe, dystopische Atmosphäre, High-Detail-Render, Lens-Flare",  # noqa: E501
    # 17. Welpen-Strandfoto
    "Nahaufnahme eines fotorealistischen Welpen mit Sonnenbrille am Sonnenuntergangsstrand, 4K HD, gestochen scharfe Details, skurrile Stimmung",  # noqa: E501
    # 18. Porträt eines erfahrenen Feuerwehrmanns
    "Porträt eines erfahrenen Feuerwehrmanns in schwerer Ausrüstung, scharfer Fokus, heroische Atmosphäre",  # noqa: E501
    # 19. Fantasy-Kanal-Ölgemälde
    "Kanal, flankiert von geschwungener Fantasy-Architektur, majestätische Komposition, Morgendämmerungsbeleuchtung, detailliert",  # noqa: E501
    # 20. Deutsches Reetdachhaus
    "Hochauflösendes Bild eines charmanten Backsteinhauses mit einem Reetdach am sandigen Ufer eines Nordseestrandes zur goldenen Stunde am Morgen. Detaillierte Ziegel- und Strohstrukturen, windgepeitschtes Dünengras im Vordergrund, weiches warmes Sonnenlicht, das natürliche Schatten wirft, subtiler Seenebel am Horizont, realistische Kameraperspektive",  # noqa: E501
]
