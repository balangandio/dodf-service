class ProcessoSentence:
    def test(self, sentence_field):
        search = re.search('^Processo$', sentence_field)
        return search != None

    def parse(self, sentence_value):
        occurrences = rs.findall('((\d+[-\.])+\d+\/\d+([-\.]\d+))?', sentence_value)

        if len(occurrences) > 0:
            ( first_occurrence, _, _ ) = occurrences[0]

        return None