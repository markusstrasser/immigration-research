/* Module only: Consumer.capitalOf returns key/response/return, not stock. */
"use strict";
function capitalAmount(component, registry, reading) {
  const matches=registry.components.filter(c=>c.id===component.id);
  if(matches.length!==1)throw Error(`[BLOCKED] missing or duplicate capital source ${component.id}`);
  const amount=matches[0].stock_charged_bn*registry.rates[reading]*component.key;
  if(!Number.isFinite(amount)||!Number.isFinite(component.response)||!Number.isFinite(component.return_bn))
    throw Error(`[BLOCKED] nonfinite capital source ${component.id}`);
  if(Math.abs(amount*component.response-component.return_bn)>1e-9)
    throw Error(`[BLOCKED] capital source does not reproduce return ${component.id}`);
  return amount;
}
module.exports={capitalAmount};
