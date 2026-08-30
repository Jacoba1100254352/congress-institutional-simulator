# LDA Medium-Priority Directional Packet Source Review

This curated review file records packet-level source review for the
medium-priority LDA disposition packets that carried support or opposition text
signals in `reports/lobbying-bill-medium-disposition-packets.csv`.

Current rows:

- 28 directional medium-priority packets.
- 25 packets came from support-signal packet status.
- 3 packets came from opposition-signal packet status.

Sources reviewed:

- Official LDA activity text preserved in the upstream exact bill-mention and
  disposition-review rows.
- Packet context and source pointers from
  `reports/lobbying-bill-medium-disposition-packets.csv`.
- Linked Congress.gov bill and Congress.gov API context already carried by the
  upstream packet rows.

Boundary:

The file records packet-level source review of activity-text disposition only.
It can confirm or narrow current-bill support/opposition text signals, but it
does not create lobbying-contact confirmation, sponsor/member targeting beyond
activity-text references, committee-action influence, roll-call influence,
legislative-outcome causality, public benefit, welfare, causal capture, or
model-validation evidence.
