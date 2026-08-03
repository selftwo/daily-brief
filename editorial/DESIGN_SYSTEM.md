# Reader system

The Daily Brief uses an **Explore → Read** surface. The publication keeps its folio, desk labels, dated archive, and source-led structure, but the story body is treated as a reading column rather than a dashboard grid.

## Visual rules

- **Paper:** cool near-white in light mode; cool slate in dark mode. No ivory, parchment, or yellowed-paper tones.
- **Ink:** softened true-gray rather than pure black or white.
- **Signal:** one calm indigo in light mode and lifted cyan in dark mode. It marks links, active controls, and live editorial signals; it is not decoration.
- **Geometry:** flat surfaces, square edges, hairline rules, and almost no shadow. Separation comes from space and rules, not cards.
- **Reading register:** serif prose at a comfortable 19px default with loose leading and a 720px / roughly 68ch measure.
- **Chrome register:** compact mono labels, uppercase only where they act as metadata or navigation.
- **Hierarchy:** headline → dek → source/date trace → summary. Desk notes and source context are progressive disclosure.
- **Responsive behavior:** the reader measure remains the priority; the issue index moves below the lead on narrow screens.
- **Interaction:** visible controls have 44px minimum targets, focus rings, reduced-motion compatibility, and no-JavaScript-safe content.

## Applied source patterns

The implementation is an original publication surface informed by the calm reader, flat single-signal, and progressive-disclosure patterns in the local design-system research. It does not reproduce a branded product shell or private app content.

## Reader registers

The hidden-by-default `Reader` panel exposes three named registers:

- **Vellum Read:** the baseline quiet reading column—cool paper, indigo signal, compact mono chrome.
- **Eddy Paper:** slightly softer headline weight, more open leading, teal signal, and margin-led spacing.
- **Tide Wander:** the most spacious register—longer leading, cooler blue-green surfaces, and relaxed headline tracking.

Text size and reading width remain independent controls. All choices persist locally and remain optional; the default edition is still readable with JavaScript disabled.

## Publication anatomy

- **Front page:** one headline and lead report with source/date/kind/status trace.
- **Sections:** typed desks such as Systems, Tools, Research, and Lifestyle; each story remains a single reading object.
- **Back page:** a derived reporting register showing the edition’s dispatch, desk, source-type, publisher, and status evidence without ranking or personalising it.
