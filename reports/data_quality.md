# Data Quality Report

## Source Summary

- raw CSV path: `data/raw/volunteer_data_en.csv`
- raw row count: `116174`
- invalid `started_at` count: `0`
- `naive=true` count: `5834`

## Modeled Daily Table

- modeled date range: `2022-02-25` to `2026-10-11`
- number of regions: `25`
- modeled oblast-date rows: `42250`

## Region List

- Cherkaska oblast
- Chernihivska oblast
- Chernivetska oblast
- Dnipropetrovska oblast
- Donetska oblast
- Ivano-Frankivska oblast
- Kharkivska oblast
- Khersonska oblast
- Khmelnytska oblast
- Kirovohradska oblast
- Kyiv City
- Kyivska oblast
- Luhanska oblast
- Lvivska oblast
- Mykolaivska oblast
- Odeska oblast
- Poltavska oblast
- Rivnenska oblast
- Sumska oblast
- Ternopilska oblast
- Vinnytska oblast
- Volynska oblast
- Zakarpatska oblast
- Zaporizka oblast
- Zhytomyrska oblast

## Raw Rows Per Region

- Cherkaska oblast: `3894`
- Chernihivska oblast: `5613`
- Chernivetska oblast: `917`
- Dnipropetrovska oblast: `13752`
- Donetska oblast: `8549`
- Ivano-Frankivska oblast: `895`
- Kharkivska oblast: `13001`
- Khersonska oblast: `6434`
- Khmelnytska oblast: `1366`
- Kirovohradska oblast: `6339`
- Kyiv City: `2673`
- Kyivska oblast: `4471`
- Luhanska oblast: `3`
- Lvivska oblast: `1798`
- Mykolaivska oblast: `7899`
- Odeska oblast: `4597`
- Poltavska oblast: `6569`
- Rivnenska oblast: `1286`
- Sumska oblast: `8744`
- Ternopilska oblast: `1015`
- Vinnytska oblast: `2093`
- Volynska oblast: `2205`
- Zakarpatska oblast: `761`
- Zaporizka oblast: `8973`
- Zhytomyrska oblast: `2327`

## Modeled Rows Per Region

- Cherkaska oblast: `1690`
- Chernihivska oblast: `1690`
- Chernivetska oblast: `1690`
- Dnipropetrovska oblast: `1690`
- Donetska oblast: `1690`
- Ivano-Frankivska oblast: `1690`
- Kharkivska oblast: `1690`
- Khersonska oblast: `1690`
- Khmelnytska oblast: `1690`
- Kirovohradska oblast: `1690`
- Kyiv City: `1690`
- Kyivska oblast: `1690`
- Luhanska oblast: `1690`
- Lvivska oblast: `1690`
- Mykolaivska oblast: `1690`
- Odeska oblast: `1690`
- Poltavska oblast: `1690`
- Rivnenska oblast: `1690`
- Sumska oblast: `1690`
- Ternopilska oblast: `1690`
- Vinnytska oblast: `1690`
- Volynska oblast: `1690`
- Zakarpatska oblast: `1690`
- Zaporizka oblast: `1690`
- Zhytomyrska oblast: `1690`

## Limitations

- This project models alert starts present in the selected dataset, not every possible real-world siren state.
- The pipeline does not infer missing alerts, correct historical reporting gaps, or adjust for special regional conditions unless they are represented in the source rows.
- The current Kyiv-local day is excluded because it may be incomplete.
- The model should not be interpreted as an operational safety or warning system.
