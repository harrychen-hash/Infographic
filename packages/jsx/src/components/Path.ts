import type { GroupProps, JSXElement, PathProps } from '../types';
import { Group } from './Group';

export function Path({ x, y, width, height, ...props }: PathProps): JSXElement {
  const node: JSXElement = {
    type: 'path',
    props,
  };

  const groupProps: GroupProps = {};
  if (x !== undefined) groupProps.x = x;
  if (y !== undefined) groupProps.y = y;
  if (width !== undefined) groupProps.width = width;
  if (height !== undefined) groupProps.height = height;
  
  // TODO scale path to fit width/height
  return Group({ ...groupProps, children: [node] });
}
