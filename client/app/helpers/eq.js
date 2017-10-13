import { helper } from "@ember/component/helper";

export function eq([param1, param2]) {
  return param1 == param2;
}

export default helper(eq);
