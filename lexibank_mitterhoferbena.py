from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomLanguage(pylexibank.Language):
    Type = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Date = attr.ib(default=None)
    Transcriber = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "mitterhoferbena"
    language_class = CustomLanguage

    form_spec = pylexibank.FormSpec(separators="/")

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )
        languages = args.writer.add_languages(id_factory=lambda l: l["Name"])

        reader = self.raw_dir.read_csv(self.raw_dir / "Wordlist.tsv", dicts=True, delimiter="\t")

        for row in pylexibank.progressbar(reader):
            lexemes = {k: v for k, v in row.items() if k in languages}
            for language, lexeme in lexemes.items():
                args.writer.add_forms_from_value(
                    Language_ID=language,
                    Parameter_ID=concepts[row["CONCEPT"]],
                    Value=lexeme,
                    Source="Mitterhofer2013",
                    Loan=False,
                )

        # We explicitly remove the ISO code column since the languages in
        # this datasets do not have an ISO code.
        args.writer.cldf["LanguageTable"].tableSchema.columns = [
            col
            for col in args.writer.cldf["LanguageTable"].tableSchema.columns
            if col.name != "ISO639P3code"
        ]
