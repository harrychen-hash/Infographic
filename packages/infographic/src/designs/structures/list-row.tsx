/** @jsxImportSource @antv/infographic-jsx */
import type { ComponentType, JSXElement } from '@antv/infographic-jsx';
import { getElementBounds, Group } from '@antv/infographic-jsx';
import { BtnAdd, BtnRemove, BtnsGroup, ItemsGroup } from '../components';
import { FlexLayout } from '../layouts';
import { registerStructure } from './registry';
import type { BaseStructureProps } from './types';

export interface ListRowProps extends BaseStructureProps {
  gap?: number;
}

export const ListRow: ComponentType<ListRowProps> = (props) => {
  const { Title, Item, data, gap = 20 } = props;
  const { title, desc, items = [] } = data;

  let height = 480;

  const titleContent = Title ? <Title title={title} desc={desc} /> : null;
  if (Title) {
    const titleBounds = getElementBounds(titleContent);
    height = titleBounds.height * 0.8;
  }

  const btnBounds = getElementBounds(<BtnAdd indexKey={'1'} />);
  const itemBounds = getElementBounds(
    <Item indexes={[0]} indexKey={'1'} data={data} datum={items[0]} />,
  );

  const btnElements: JSXElement[] = [];
  const itemElements: JSXElement[] = [];

  const btnAddY = (height - btnBounds.height) / 2;
  items.forEach((item, index) => {
    const indexKey = `${index + 1}`;
    const itemX = (itemBounds.width + gap) * index;

    itemElements.push(
      <Item
        indexes={[index]}
        id={`item-${indexKey}`}
        datum={item}
        data={data}
        x={itemX}
        height={height}
        positionH="center"
      />,
    );

    btnElements.push(
      <BtnRemove
        indexKey={indexKey}
        id={`btn-remove-${indexKey}`}
        x={itemX + (itemBounds.width - btnBounds.width) / 2}
        y={-btnBounds.height - 10}
      />,
    );

    btnElements.push(
      <BtnAdd
        indexKey={indexKey}
        id={`btn-add-${indexKey}`}
        x={itemX - btnBounds.width}
        y={btnAddY}
      />,
    );
  });

  if (items.length > 0) {
    const lastItemX = (itemBounds.width + gap) * (items.length - 1);
    const extraAddBtnX = lastItemX + itemBounds.width;

    btnElements.push(
      <BtnAdd
        indexKey={`${items.length + 1}`}
        id={`btn-add-${items.length + 1}`}
        x={extraAddBtnX}
        y={btnAddY}
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
        <ItemsGroup>{itemElements}</ItemsGroup>
        <BtnsGroup>{btnElements}</BtnsGroup>
      </Group>
    </FlexLayout>
  );
};

registerStructure('list-row', { component: ListRow });
