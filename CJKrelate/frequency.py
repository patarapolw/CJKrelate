from abc import ABCMeta, abstractmethod


class AbstractFrequency(metaclass=ABCMeta):
    entries = NotImplemented    # type: dict

    @abstractmethod
    def __init__(self):
        """
        self.entries[source] = list of [char, count, relative_frequency]
        self.entries[source][0] = ["all", total_count, 1]
        """
        if self.entries is NotImplemented:
            raise NotImplementedError

        self.all_sources = self.merge_sources()

    def relative_freq(self, char, source=None):
        if source:
            entries = self.entries[source]
        else:
            entries = self.all_sources

        for entry in entries:
            if entry[0] == char:
                return entry[2]

        return 0

    def listing(self, char):
        for source, file_content in self.entries.items():
            for i, entry in enumerate(file_content):
                if entry[0] == char:
                    yield source, i

    def merge_sources(self):
        all_chars = dict()
        row_1 = row_2 = 0
        number_of_files = len(self.entries)
        for file_content in self.entries.values():
            for row in file_content:
                all_chars.setdefault(row[0], [row[0], row_1, row_2])
                all_chars[row[0]][1] += row[1] / number_of_files
                all_chars[row[0]][2] += row[2] / number_of_files

        return sorted(all_chars.values(), key=lambda x: x[1], reverse=True)

