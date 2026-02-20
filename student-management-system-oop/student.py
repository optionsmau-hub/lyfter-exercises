class Student:
    def __init__(self, name: str, section: str, scores: dict[str, float] | None = None):
        self.name = name
        self.section = section
        self.scores = scores or {}
        self.average = self.calculate_average()

    def calculate_average(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)

    def to_dict(self, subjects: list[str]) -> dict:
        """
        Convert Student object into a dict compatible with CSV export.
        Ensures all subjects exist as columns.
        """
        row = {
            "name": self.name,
            "section": self.section,
            "average": f"{self.average:.2f}",
        }

        for subject in subjects:
            row[subject] = self.scores.get(subject, "")

        return row

    @classmethod
    def from_dict(cls, data: dict, subjects: list[str]):
        """
        Convert a CSV row (dict) into a Student object.
        """
        scores = {}
        for subject in subjects:
            value = data.get(subject, "")
            if value != "" and value is not None:
                scores[subject] = float(value)

        student = cls(
            name=data.get("name", ""),
            section=data.get("section", ""),
            scores=scores
        )

        # If your CSV already has average, you can trust it OR recompute it.
        # We'll recompute to keep it consistent.
        student.average = student.calculate_average()
        return student