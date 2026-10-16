# Encountered acquisition failures

- **Census response was an HTML missing-key page.** HTTP success was not data
  success. Retried using the repository's authorized Census key without printing
  it. Only validated JSON tables were staged; original-body hashes precede all
  analysis. `test_nondata_api_response_is_rejected` rejects HTML, objects, empty
  arrays and empty headers; duplicate headers must also agree before collapse.
- **Interrupted original ZIP download.** The partial archive failed validation.
  Resumed acquisition and validated its ZIP directory and members before staging
  its final hash. The staffing estimates use independently validated published
  API aggregates, not partially downloaded unit records. ZIP is retained as
  original documentation and is not an analytical input.
- **Unordered validation receipts.** A set iteration changed the order of the
  employment check rows between fresh Python processes, although estimates were
  identical. Sort FIPS before generating checks. The independent-process byte
  replay includes the entire checks JSON and fails if its order changes.

Neither failure is evidence about the assumption being audited.
