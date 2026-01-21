"""
Auto-generated field mappings for VIDEX form automation.
Maps JSON field keys to CSS selectors.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FieldMapping:
    """Represents a field mapping for form automation."""
    field_id: str
    selector: str
    field_type: str
    required: bool
    section: str = ""
    label: str = ""


# Field mappings organized by section
FIELD_MAPPINGS: dict[int, list[FieldMapping]] = {
    # Section 0: Personal Data
    0: [
        FieldMapping(
            field_id="antragsteller.familienname",
            selector="[id="antragsteller.familienname"]",
            field_type="text",
            required=False,
            label="Family name",
        ),
        FieldMapping(
            field_id="antragsteller.geburtsname",
            selector="[id="antragsteller.geburtsname"]",
            field_type="text",
            required=False,
            label="Name at birth",
        ),
        FieldMapping(
            field_id="antragsteller.vorname",
            selector="[id="antragsteller.vorname"]",
            field_type="text",
            required=False,
            label="First name(s)",
        ),
        FieldMapping(
            field_id="antragsteller.geburtsdatum",
            selector="[id="antragsteller.geburtsdatum"]",
            field_type="text",
            required=False,
            label="Date of birth (dd.mm.yyyy)",
        ),
        FieldMapping(
            field_id="antragsteller.geburtsort",
            selector="[id="antragsteller.geburtsort"]",
            field_type="text",
            required=False,
            label="Place of birth",
        ),
        FieldMapping(
            field_id="rechtAufFreizuegigkeit",
            selector="[id="rechtAufFreizuegigkeit"]",
            field_type="checkbox",
            required=False,
            label="Yes",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.firmenname",
            selector="[id="antragsteller.personendaten.berufdaten.firmenname"]",
            field_type="text",
            required=False,
            label="Company name and telephone number (for students name and telephone number of educational establishment)",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.strasse",
            selector="[id="antragsteller.personendaten.berufdaten.strasse"]",
            field_type="text",
            required=False,
            label="Street",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.hausnummer",
            selector="[id="antragsteller.personendaten.berufdaten.hausnummer"]",
            field_type="text",
            required=False,
            label="House number",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.sonstigeAdressangaben",
            selector="[id="antragsteller.personendaten.berufdaten.sonstigeAdressangaben"]",
            field_type="text",
            required=False,
            label="Other address information",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.plz",
            selector="[id="antragsteller.personendaten.berufdaten.plz"]",
            field_type="text",
            required=False,
            label="Postal code",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.ort",
            selector="[id="antragsteller.personendaten.berufdaten.ort"]",
            field_type="text",
            required=False,
            label="Town/city",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.strasse",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.strasse"]",
            field_type="text",
            required=False,
            label="Street",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.hausnummer",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.hausnummer"]",
            field_type="text",
            required=False,
            label="House number",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.sonstigeAdressangaben",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.sonstigeAdressangaben"]",
            field_type="text",
            required=False,
            label="Other address information",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.plz",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.plz"]",
            field_type="text",
            required=False,
            label="Postal code",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.ort",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.ort"]",
            field_type="text",
            required=False,
            label="Town/city",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.kontaktdaten.telefon",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.kontaktdaten.telefon"]",
            field_type="text",
            required=False,
            label="Telephone/mobile number",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.kontaktdaten.email",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.kontaktdaten.email"]",
            field_type="text",
            required=False,
            label="Email",
        ),
        FieldMapping(
            field_id="antragsteller.aufenthaltsberechtigung",
            selector="[id="antragsteller.aufenthaltsberechtigung"]",
            field_type="checkbox",
            required=False,
            label="Is your residence in a country other than that of your current nationality?",
        ),
        FieldMapping(
            field_id="antragsteller.pass.passnummer",
            selector="[id="antragsteller.pass.passnummer"]",
            field_type="text",
            required=False,
            label="Travel document number",
        ),
        FieldMapping(
            field_id="antragsteller.nationaleIdentNr",
            selector="[id="antragsteller.nationaleIdentNr"]",
            field_type="text",
            required=False,
            label="National identity number, where applicable",
        ),
        FieldMapping(
            field_id="antragsteller.pass.gueltigVon",
            selector="[id="antragsteller.pass.gueltigVon"]",
            field_type="text",
            required=False,
            label="Date of issue (dd.mm.yyyy)",
        ),
        FieldMapping(
            field_id="antragsteller.pass.gueltigBis",
            selector="[id="antragsteller.pass.gueltigBis"]",
            field_type="text",
            required=False,
            label="Valid until (dd.mm.yyyy)",
        ),
        FieldMapping(
            field_id="antragsteller.pass.ausgestelltVon",
            selector="[id="antragsteller.pass.ausgestelltVon"]",
            field_type="text",
            required=False,
            label="Issued by",
        ),
        FieldMapping(
            field_id="antragsteller.pass.ausgestelltIn",
            selector="[id="antragsteller.pass.ausgestelltIn"]",
            field_type="text",
            required=False,
            label="Issued in",
        ),
        FieldMapping(
            field_id="antragsteller.biometrie.fingerabdrueckeErfassungsDatum_vorhanden",
            selector="[id="antragsteller.biometrie.fingerabdrueckeErfassungsDatum_vorhanden"]",
            field_type="checkbox",
            required=False,
            label="Yes",
        ),
        FieldMapping(
            field_id="reisedaten.letzteVisumStickernummer",
            selector="[id="reisedaten.letzteVisumStickernummer"]",
            field_type="checkbox",
            required=False,
            label="Visa sticker number, if known",
        ),
        FieldMapping(
            field_id="reisedaten.angegebenerReisezweck",
            selector="[id="reisedaten.angegebenerReisezweck"]",
            field_type="text",
            required=False,
            label="Other (please specify)",
        ),
        FieldMapping(
            field_id="reisedaten.weitereInformationen",
            selector="[id="reisedaten.weitereInformationen"]",
            field_type="text",
            required=False,
            label="Further information on the purpose of the stay",
        ),
        FieldMapping(
            field_id="visumdaten.gueltigkeit.von",
            selector="[id="visumdaten.gueltigkeit.von"]",
            field_type="text",
            required=False,
            label="Intended date of arrival for the first intended stay in the Schengen area",
        ),
        FieldMapping(
            field_id="visumdaten.gueltigkeit.bisGenau.value",
            selector="[id="visumdaten.gueltigkeit.bisGenau.value"]",
            field_type="text",
            required=False,
            label="Intended date of departure from the Schengen area after the first intended stay",
        ),
        FieldMapping(
            field_id="antragsteller.einreisegenehmigung.einreisegenehmigungsNr",
            selector="[id="antragsteller.einreisegenehmigung.einreisegenehmigungsNr"]",
            field_type="text",
            required=False,
            label="Entry permit number",
        ),
        FieldMapping(
            field_id="antragsteller.einreisegenehmigung.ausgestelltVon",
            selector="[id="antragsteller.einreisegenehmigung.ausgestelltVon"]",
            field_type="text",
            required=False,
            label="Issued by",
        ),
        FieldMapping(
            field_id="antragsteller.einreisegenehmigung.gueltigVon",
            selector="[id="antragsteller.einreisegenehmigung.gueltigVon"]",
            field_type="text",
            required=False,
            label="Valid from (dd.mm.yyyy)",
        ),
        FieldMapping(
            field_id="antragsteller.einreisegenehmigung.gueltigBis",
            selector="[id="antragsteller.einreisegenehmigung.gueltigBis"]",
            field_type="text",
            required=False,
            label="Valid until (dd.mm.yyyy)",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.familienname",
            selector="[id="referenz.ansprechpartner.familienname"]",
            field_type="text",
            required=False,
            label="Family name",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.vorname",
            selector="[id="referenz.ansprechpartner.vorname"]",
            field_type="text",
            required=False,
            label="First name(s)",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.geburtsdatum",
            selector="[id="referenz.ansprechpartner.geburtsdatum"]",
            field_type="text",
            required=False,
            label="Date of birth (dd.mm.yyyy)",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.geburtsort",
            selector="[id="referenz.ansprechpartner.geburtsort"]",
            field_type="text",
            required=False,
            label="Place of birth",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.anschrift.strasse",
            selector="[id="referenz.ansprechpartner.anschrift.strasse"]",
            field_type="text",
            required=False,
            label="Street",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.anschrift.hausnummer",
            selector="[id="referenz.ansprechpartner.anschrift.hausnummer"]",
            field_type="text",
            required=False,
            label="House number",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.anschrift.plz",
            selector="[id="referenz.ansprechpartner.anschrift.plz"]",
            field_type="text",
            required=False,
            label="Postal code",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.anschrift.ort",
            selector="[id="referenz.ansprechpartner.anschrift.ort"]",
            field_type="text",
            required=False,
            label="Town/city",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.kontaktdaten.telefon",
            selector="[id="referenz.ansprechpartner.kontaktdaten.telefon"]",
            field_type="text",
            required=False,
            label="Telephone/mobile number",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.kontaktdaten.email",
            selector="[id="referenz.ansprechpartner.kontaktdaten.email"]",
            field_type="text",
            required=False,
            label="Email",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.abweichendeSchreibweiseNachname",
            selector="[id="referenz.ansprechpartner.abweichendeSchreibweiseNachname"]",
            field_type="text",
            required=False,
            label="Alternative spelling - surname(s)",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.abweichendeSchreibweiseVorname",
            selector="[id="referenz.ansprechpartner.abweichendeSchreibweiseVorname"]",
            field_type="text",
            required=False,
            label="Alternative spelling - first name(s)",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.andereNamen",
            selector="[id="referenz.ansprechpartner.andereNamen"]",
            field_type="text",
            required=False,
            label="Other names",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.fruehereNamen",
            selector="[id="referenz.ansprechpartner.fruehereNamen"]",
            field_type="text",
            required=False,
            label="Previous names",
        ),
        FieldMapping(
            field_id="reisedaten.reisekostenUebernahme.antragsteller",
            selector="[id="reisedaten.reisekostenUebernahme.antragsteller"]",
            field_type="checkbox",
            required=False,
            label="the applicant him/herself",
        ),
        FieldMapping(
            field_id="reisedaten.reisekostenUebernahme.dritte",
            selector="[id="reisedaten.reisekostenUebernahme.dritte"]",
            field_type="checkbox",
            required=False,
            label="a third party (host, company, organisation), please specify",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.bar",
            selector="[id="reisedaten.lebensunterhalt.bar"]",
            field_type="checkbox",
            required=False,
            label="Cash",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.reiseschecks",
            selector="[id="reisedaten.lebensunterhalt.reiseschecks"]",
            field_type="checkbox",
            required=False,
            label="Traveller's cheques",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.kreditkarten",
            selector="[id="reisedaten.lebensunterhalt.kreditkarten"]",
            field_type="checkbox",
            required=False,
            label="Credit cards",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.unterkunft",
            selector="[id="reisedaten.lebensunterhalt.unterkunft"]",
            field_type="checkbox",
            required=False,
            label="Accommodation paid in advance",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.vollstaendigeKostenuebernahme",
            selector="[id="reisedaten.lebensunterhalt.vollstaendigeKostenuebernahme"]",
            field_type="checkbox",
            required=False,
            label="Assumption of all expenses during the stay",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.befoerderung",
            selector="[id="reisedaten.lebensunterhalt.befoerderung"]",
            field_type="checkbox",
            required=False,
            label="Transport paid in advance",
        ),
        FieldMapping(
            field_id="reisedaten.lebensunterhalt.sonstiges",
            selector="[id="reisedaten.lebensunterhalt.sonstiges"]",
            field_type="checkbox",
            required=False,
            label="Other (please specify)",
        ),
        FieldMapping(
            field_id="antragsteller.geburtsland",
            selector="[id="antragsteller.geburtsland"]",
            field_type="select",
            required=False,
            label="Country of birth",
        ),
        FieldMapping(
            field_id="antragsteller.geschlecht",
            selector="[id="antragsteller.geschlecht"]",
            field_type="select",
            required=False,
            label="Sex",
        ),
        FieldMapping(
            field_id="antragsteller.familienstand",
            selector="[id="antragsteller.familienstand"]",
            field_type="select",
            required=False,
            label="Marital status",
        ),
        FieldMapping(
            field_id="antragsteller.staatsangehoerigkeitListe[0]",
            selector="[id="antragsteller.staatsangehoerigkeitListe[0]"]",
            field_type="select",
            required=False,
            label="Current nationality",
        ),
        FieldMapping(
            field_id="antragsteller.staatsangehoerigkeitBeiGeburtListe[0]",
            selector="[id="antragsteller.staatsangehoerigkeitBeiGeburtListe[0]"]",
            field_type="select",
            required=False,
            label="Original nationality",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.berufAuswahl",
            selector="[id="antragsteller.personendaten.berufdaten.berufAuswahl"]",
            field_type="select",
            required=False,
            label="Current occupation",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.berufdaten.land",
            selector="[id="antragsteller.personendaten.berufdaten.land"]",
            field_type="select",
            required=False,
            label="Country",
        ),
        FieldMapping(
            field_id="antragsteller.personendaten.staendigeAnschrift.land",
            selector="[id="antragsteller.personendaten.staendigeAnschrift.land"]",
            field_type="select",
            required=False,
            label="Country",
        ),
        FieldMapping(
            field_id="antragsteller.pass.passArt",
            selector="[id="antragsteller.pass.passArt"]",
            field_type="select",
            required=False,
            label="Type of travel document",
        ),
        FieldMapping(
            field_id="antragsteller.pass.ausstellenderStaat",
            selector="[id="antragsteller.pass.ausstellenderStaat"]",
            field_type="select",
            required=False,
            label="Issuing state",
        ),
        FieldMapping(
            field_id="reisedaten.aufenthaltszweckListe[0]",
            selector="[id="reisedaten.aufenthaltszweckListe[0]"]",
            field_type="select",
            required=False,
            label="Purpose(s) of the journey",
        ),
        FieldMapping(
            field_id="reisedaten.ersteinreiseStaat",
            selector="[id="reisedaten.ersteinreiseStaat"]",
            field_type="select",
            required=False,
            label="Member State of first entry",
        ),
        FieldMapping(
            field_id="reisedaten.hauptzielListe[0]",
            selector="[id="reisedaten.hauptzielListe[0]"]",
            field_type="select",
            required=False,
            label="Main travel destination(s)",
        ),
        FieldMapping(
            field_id="visumdaten.anzahlEinreisen",
            selector="[id="visumdaten.anzahlEinreisen"]",
            field_type="select",
            required=False,
            label="Number of entries requested",
        ),
        FieldMapping(
            field_id="antragsteller.einreisegenehmigung.artDerEinreisegenehmigungAuswahl",
            selector="[id="antragsteller.einreisegenehmigung.artDerEinreisegenehmigungAuswahl"]",
            field_type="select",
            required=False,
            label="Type of entry permit",
        ),
        FieldMapping(
            field_id="antragsteller.einreisegenehmigung.endzielStaat",
            selector="[id="antragsteller.einreisegenehmigung.endzielStaat"]",
            field_type="select",
            required=False,
            label="Final country of destination",
        ),
        FieldMapping(
            field_id="referenz.referenzArt",
            selector="[id="referenz.referenzArt"]",
            field_type="select",
            required=False,
            label="Type of reference",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.geschlecht",
            selector="[id="referenz.ansprechpartner.geschlecht"]",
            field_type="select",
            required=False,
            label="Sex",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.staatsangehoerigkeit",
            selector="[id="referenz.ansprechpartner.staatsangehoerigkeit"]",
            field_type="select",
            required=False,
            label="Nationality",
        ),
        FieldMapping(
            field_id="referenz.ansprechpartner.anschrift.land",
            selector="[id="referenz.ansprechpartner.anschrift.land"]",
            field_type="select",
            required=False,
            label="Country",
        ),
    ],
    # Section 1: Contact Details
    1: [
    ],
    # Section 2: Documents
    2: [
    ],
    # Section 3: Travel Data
    3: [
    ],
    # Section 4: Reference
    4: [
    ],
    # Section 5: Cost Coverage
    5: [
    ],
}


# Flat mapping: field_id -> FieldMapping
FLAT_MAPPINGS: dict[str, FieldMapping] = {
    mapping.field_id: mapping
    for mappings in FIELD_MAPPINGS.values()
    for mapping in mappings
}


def get_selector(field_id: str) -> Optional[str]:
    """Get the CSS selector for a field ID."""
    mapping = FLAT_MAPPINGS.get(field_id)
    return mapping.selector if mapping else None


def get_required_fields() -> list[str]:
    """Get list of all required field IDs."""
    return [m.field_id for m in FLAT_MAPPINGS.values() if m.required]
