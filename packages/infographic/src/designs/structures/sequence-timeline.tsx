/** @jsxImportSource @antv/infographic-jsx */
import type { ComponentType, JSXElement } from '@antv/infographic-jsx';
import {
  Ellipse,
  getElementBounds,
  Group,
  Path,
  Text,
} from '@antv/infographic-jsx';
import { BtnAdd, BtnRemove, BtnsGroup, ItemsGroup } from '../components';
import { FlexLayout } from '../layouts';
import { getColorPrimary, getPaletteColors } from '../utils';
import { registerStructure } from './registry';
import type { BaseStructureProps } from './types';

export interface SequenceTimelineProps extends BaseStructureProps {
  gap?: number;
  lineOffset?: number;
}

const STEP_LABELS = [
  'STEP 1',
  'STEP 2',
  'STEP 3',
  'STEP 4',
  'STEP 5',
  'STEP 6',
  'STEP 7',
  'STEP 8',
  'STEP 9',
  'STEP 10',
  'STEP 11',
  'STEP 12',
  'STEP 13',
  'STEP 14',
  'STEP 15',
  'STEP 16',
  'STEP 17',
  'STEP 18',
  'STEP 19',
  'STEP 20',
];

export const SequenceTimeline: ComponentType<SequenceTimelineProps> = (
  props,
) => {
  const { Title, Item, data, gap = 10, options } = props;
  const { title, desc, items = [] } = data;

  const titleContent = Title ? <Title title={title} desc={desc} /> : null;
  const colorPrimary = getColorPrimary(options);
  const palette = getPaletteColors(options);
  const btnBounds = getElementBounds(<BtnAdd indexes={[0]} />);
  const itemBounds = getElementBounds(
    <Item indexes={[0]} data={data} datum={items[0]} positionH="normal" />,
  );

  const btnElements: JSXElement[] = [];
  const itemElements: JSXElement[] = [];
  const decorElements: JSXElement[] = [];

  const stepLabelX = 10;
  const timelineX = stepLabelX + 70 + 10;
  const itemX = timelineX + 30;
  const nodeRadius = 6;

  // Add continuous timeline line first (so it appears behind the dots)
  if (items.length > 1) {
    const firstNodeY = itemBounds.height / 2 + nodeRadius;
    const lastNodeY =
      (items.length - 1) * (itemBounds.height + gap) +
      itemBounds.height / 2 -
      nodeRadius;
    const continuousLinePath = `M ${timelineX} ${firstNodeY} L ${timelineX} ${lastNodeY}`;

    decorElements.push(
      <Path
        d={continuousLinePath}
        stroke={colorPrimary}
        strokeWidth={2}
        width={1}
        height={lastNodeY - firstNodeY}
      />,
    );
  }

  items.forEach((item, index) => {
    const itemY = index * (itemBounds.height + gap);
    const nodeY = itemY + itemBounds.height / 2;
    const indexes = [index];

    decorElements.push(
      <Text
        x={stepLabelX}
        y={nodeY}
        width={70}
        fontSize={18}
        fontWeight="bold"
        alignHorizontal="left"
        alignVertical="center"
        fill={palette[index % palette.length]}
      >
        {STEP_LABELS[index] || `STEP ${index + 1}`}
      </Text>,
    );

    itemElements.push(
      <Item
        indexes={indexes}
        datum={item}
        data={data}
        x={itemX}
        y={itemY}
        positionH="normal"
      />,
    );

    decorElements.push(
      <Ellipse
        x={timelineX - nodeRadius}
        y={nodeY - nodeRadius}
        width={nodeRadius * 2}
        height={nodeRadius * 2}
        fill={palette[index % palette.length]}
      />,
    );

    btnElements.push(
      <BtnRemove
        indexes={indexes}
        x={itemX - btnBounds.width - 10}
        y={itemY + (itemBounds.height - btnBounds.height) / 2}
      />,
    );

    if (index === 0) {
      btnElements.push(
        <BtnAdd
          indexes={indexes}
          x={itemX + (itemBounds.width - btnBounds.width) / 2}
          y={itemY - btnBounds.height - 10}
        />,
      );
    } else {
      btnElements.push(
        <BtnAdd
          indexes={indexes}
          x={itemX + (itemBounds.width - btnBounds.width) / 2}
          y={itemY - gap / 2 - btnBounds.height / 2}
        />,
      );
    }
  });

  if (items.length > 0) {
    const lastItemY = (items.length - 1) * (itemBounds.height + gap);
    btnElements.push(
      <BtnAdd
        indexes={[items.length]}
        x={itemX + (itemBounds.width - btnBounds.width) / 2}
        y={lastItemY + itemBounds.height + 10}
      />,
    );
  }

  return (
    <FlexLayout
      id="infographic-container"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
    >
      {titleContent}
      <Group>
        <Group>{decorElements}</Group>
        <ItemsGroup>{itemElements}</ItemsGroup>
        <BtnsGroup>{btnElements}</BtnsGroup>
      </Group>
    </FlexLayout>
  );
};

registerStructure('sequence-timeline', { component: SequenceTimeline });
