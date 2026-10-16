# Send-back summary for Tito (Stage 1 and Stage 2)

Paste this under the 1NF/2NF sections, for example as a short "Verification" paragraph at the end of Stage 2.

---

**Verification (Cedric).** We traced raw rows 1, 9 and 15 into the 1NF file by hand and checked all 15 raw
rows with a script: each produces exactly the product of its list sizes (32, 4 and 4 rows; 280 in total),
every skill, certification, phone, material and equipment value appears with nothing extra, and every
material and equipment item keeps its own cost (Concrete is always 120 on P001, never 300). The five 2NF
entity and price tables have no duplicate rows or duplicate keys, their values match the raw file, every
foreign key points to an existing row, and joining the six 2NF tables rebuilds the 1NF file exactly, so the
decomposition is lossless. We also found that a smaller set of columns happens to be unique in this sample,
so the 1NF key is justified by what each row means rather than by the sample, and that
(ProjectID, MaterialSupplied) happens to determine the unit cost because only P004 buys one material from two
suppliers; the Stage 1 and Stage 2 wording was corrected to say this.

---

Also send Tito [findings_and_corrections.md](findings_and_corrections.md): it has the two replacement
paragraphs to paste into Stage 1 and Stage 2 before the PDF is exported again.
