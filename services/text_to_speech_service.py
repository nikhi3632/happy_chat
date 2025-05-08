from services.services import get_tts_model

def synthesize_speech(text: str, output_path: str, speaker: str, language: str = "en") -> str:
    tts_model = get_tts_model()
    tts_model.tts_to_file(text=text, file_path=output_path, speaker=speaker, language=language)
    return output_path

# Available Speakers
# [
    # 'Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 
    #  'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 
    #  'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 
    #  'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 
    #  'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 
    #  'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 
    #  'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 
    #  'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström',
    #  'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa',
    #  'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 
    #  'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 
    #  'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski'
#]

# Available Languages
# [
    # 'en', 'es', 'fr', 'de', 
    # 'it', 'pt', 'pl', 'tr', 
    # 'ru', 'nl', 'cs', 'ar', 
    # 'zh-cn', 
    # 'hu', 'ko', 'ja', 'hi'
#]
