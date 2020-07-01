from mal import config
from mal.search import _Search, _SearchResult


class AnimeSearchResult(_SearchResult):
    def __init__(self, image_url, title, synopsis, media_type, episodes, score):
        super().__init__(image_url, title, synopsis, media_type, score)
        self.episodes = episodes


class AnimeSearch(_Search):
    def __init__(self, query, timeout=config.TIMEOUT):
        super().__init__(query, "anime", timeout)

    @property
    def results(self):
        try:
            self._results
        except AttributeError:
            trs = self._inner_page.find_all("tr")
            results = []
            for tr in trs[1:]:
                tds = tr.find_all("td")
                results.append(AnimeSearchResult(
                    image_url=tds[0].find("img")["data-src"],
                    title=tds[1].find("strong").text.strip(),
                    synopsis=self._remove_suffix(tds[1].find("div", {"class": "pt4"}).text.strip(), "read more."),
                    media_type=tds[2].text.strip(),
                    episodes=self._parse_eps_vols(tds[3].text),
                    score=self._parse_score(tds[4].text)
                ))
            self._results = results
        return self._results