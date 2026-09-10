# Demo prompt files — Urban Plan Generator (MiniGPT)

Use these with the **Attach text file** button on the Urban Plan Generator page.
Each file is a single prompt in the format the character-level model was trained on:

    Context: <one sentence describing the ward>.
    Recommendations:
    -

| File | Scenario |
|---|---|
| ward_it_corridor.txt | dense IT-office ward, waterlogging, low green cover |
| ward_floodplain_riverside.txt | Mula-Mutha riverside, informal settlements, unprotected frontage |
| ward_heritage_core.txt | old-city heritage core, narrow lanes, very high density |
| ward_periurban_growth.txt | city-fringe village, mostly agricultural, no drainage |
| ward_dense_residential.txt | general residential ward with natural drainage |

Attach a file → it loads into the prompt box → click **Generate Recommendations**.
Temperature ~0.8 gives balanced output; lower (0.6) is safer, higher (1.2) more varied.
