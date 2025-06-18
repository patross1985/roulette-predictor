"""Incident Logger for Canadian Law References.

This script allows the user to log incident descriptions. It scans the text for
predefined keywords such as "emotional abuse" or "privacy breach" and maps
those keywords to relevant Canadian laws. It then outputs a short affidavit
style statement summarizing the incident and the potentially applicable law.

The mapping is not exhaustive and does not constitute legal advice. It merely
provides a simple association between key phrases and well known Canadian
statutes such as the Canadian Charter of Rights and Freedoms ("Charter"), the
Child, Youth and Family Enhancement Act ("CYFEA"), and the Freedom of
Information and Protection of Privacy Act ("FOIP").
"""

from __future__ import annotations

import datetime
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Incident:
    description: str
    detected_laws: List[str]
    timestamp: datetime.datetime

    def to_affidavit(self) -> str:
        """Return a formatted affidavit style statement."""
        date_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        law_list = ", ".join(self.detected_laws) if self.detected_laws else "None"
        return (
            f"AFFIDAVIT\n"
            f"Date: {date_str}\n"
            f"Description: {self.description}\n"
            f"Potentially Relevant Law(s): {law_list}\n"
        )


KEYWORD_TO_LAW: Dict[str, str] = {
    "emotional abuse": "CYFEA (Child, Youth and Family Enhancement Act)",
    "privacy breach": "FOIP (Freedom of Information and Protection of Privacy Act)",
    "freedom": "Charter (Canadian Charter of Rights and Freedoms)",
}


def detect_laws(text: str) -> List[str]:
    """Detect relevant laws based on keywords in the text."""
    laws: List[str] = []
    lowered = text.lower()
    for keyword, law in KEYWORD_TO_LAW.items():
        if keyword in lowered:
            laws.append(law)
    return laws


def log_incident(description: str) -> Incident:
    """Create an Incident object from the description."""
    detected = detect_laws(description)
    return Incident(description=description, detected_laws=detected, timestamp=datetime.datetime.now())


def main(args: Optional[List[str]] = None) -> None:
    if args is None:
        args = sys.argv[1:]

    if args:
        description = " ".join(args)
    else:
        description = input("Describe the incident: ")

    incident = log_incident(description)
    print(incident.to_affidavit())


if __name__ == "__main__":
    main()
