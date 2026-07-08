from csp.csp import CSP
from csp.backtracking import backtracking, backtracking_all
from csp.util import timed_run, print_section


def mapColoring(
    locations: dict[str, list[str]],
    colors: list[str],
    inference="none",
    lcv=False,
    solver=backtracking,
):
    c = CSP()

    domain = list(dict.fromkeys(colors))

    for location in locations:
        c.addVariable(location, domain)

    seen_edges = set()

    for location, neighbors in locations.items():
        for neighbor in neighbors:
            if location == neighbor:
                continue

            edge = frozenset((location, neighbor))

            if edge in seen_edges:
                continue

            seen_edges.add(edge)

            c.addBinaryConstraint(location, neighbor, lambda a, b: a != b)

    return solver(c, inference=inference, lcv=lcv)


US_CONTIGUOUS_LOCATIONS = {
    "AL": ["FL", "GA", "MS", "TN"],
    "AZ": ["CA", "CO", "NV", "NM", "UT"],
    "AR": ["LA", "MS", "MO", "OK", "TN", "TX"],
    "CA": ["AZ", "NV", "OR"],
    "CO": ["AZ", "KS", "NE", "NM", "OK", "UT", "WY"],
    "CT": ["MA", "NY", "RI"],
    "DE": ["MD", "NJ", "PA"],
    "FL": ["AL", "GA"],
    "GA": ["AL", "FL", "NC", "SC", "TN"],
    "ID": ["MT", "NV", "OR", "UT", "WA", "WY"],
    "IL": ["IA", "IN", "KY", "MO", "WI"],
    "IN": ["IL", "KY", "MI", "OH"],
    "IA": ["IL", "MN", "MO", "NE", "SD", "WI"],
    "KS": ["CO", "MO", "NE", "OK"],
    "KY": ["IL", "IN", "MO", "OH", "TN", "VA", "WV"],
    "LA": ["AR", "MS", "TX"],
    "ME": ["NH"],
    "MD": ["DE", "PA", "VA", "WV"],
    "MA": ["CT", "NH", "NY", "RI", "VT"],
    "MI": ["IN", "OH", "WI"],
    "MN": ["IA", "ND", "SD", "WI"],
    "MS": ["AL", "AR", "LA", "TN"],
    "MO": ["AR", "IA", "IL", "KS", "KY", "NE", "OK", "TN"],
    "MT": ["ID", "ND", "SD", "WY"],
    "NE": ["CO", "IA", "KS", "MO", "SD", "WY"],
    "NV": ["AZ", "CA", "ID", "OR", "UT"],
    "NH": ["MA", "ME", "VT"],
    "NJ": ["DE", "NY", "PA"],
    "NM": ["AZ", "CO", "OK", "TX", "UT"],
    "NY": ["CT", "MA", "NJ", "PA", "VT"],
    "NC": ["GA", "SC", "TN", "VA"],
    "ND": ["MN", "MT", "SD"],
    "OH": ["IN", "KY", "MI", "PA", "WV"],
    "OK": ["AR", "CO", "KS", "MO", "NM", "TX"],
    "OR": ["CA", "ID", "NV", "WA"],
    "PA": ["DE", "MD", "NJ", "NY", "OH", "WV"],
    "RI": ["CT", "MA"],
    "SC": ["GA", "NC"],
    "SD": ["IA", "MN", "MT", "ND", "NE", "WY"],
    "TN": ["AL", "AR", "GA", "KY", "MS", "MO", "NC", "VA"],
    "TX": ["AR", "LA", "NM", "OK"],
    "UT": ["AZ", "CO", "ID", "NV", "NM", "WY"],
    "VT": ["MA", "NH", "NY"],
    "VA": ["KY", "MD", "NC", "TN", "WV"],
    "WA": ["ID", "OR"],
    "WV": ["KY", "MD", "OH", "PA", "VA"],
    "WI": ["IA", "IL", "MI", "MN"],
    "WY": ["CO", "ID", "MT", "NE", "SD", "UT"],
}


def unitedStatesMapColoring():
    colors = ["red", "green", "blue", "yellow"]

    result = mapColoring(
        US_CONTIGUOUS_LOCATIONS,
        colors,
        inference="ac3",
        lcv=True,
    )

    print(result)


australia = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Q"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "Q": ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V": ["SA", "NSW"],
    "T": [],
}


def australiaFunc():
    colors = ["red", "green", "blue"]

    result = mapColoring(australia, colors, inference="ac3")

    print(result)


def main():
    for k in range(1, 5):
        colors = list(range(k))
        result = mapColoring(US_CONTIGUOUS_LOCATIONS, colors, inference="ac3")

        if result is not None:
            print(f"Minimum colors found for American Map: {k}")
            break

    for k in range(1, 5):
        colors = list(range(k))
        result = mapColoring(australia, colors, inference="ac3")

        if result is not None:
            print(f"Minimum colors found for Australian Map: {k}")
            break


if __name__ == "__main__":
    main()
