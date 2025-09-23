/** @jsxImportSource @antv/infographic-jsx */
import { ComponentType, getElementBounds, Group } from '@antv/infographic-jsx';
import { ItemDesc, ItemIcon, ItemLabel } from '../components';
import { FlexLayout } from '../layouts';
import { registerItem } from './registry';
import type { BaseItemProps } from './types';
import { getItemProps } from './utils';

export interface SimpleItemProps extends BaseItemProps {
  width?: number;
  gap?: number;
  iconSize?: number;
}

export const SimpleItem: ComponentType<SimpleItemProps> = (props) => {
  const [
    {
      indexes,
      datum,
      width = 200,
      gap = 4,
      iconSize = 30,
      positionH = 'normal',
      positionV = 'normal',
    },
    restProps,
  ] = getItemProps(props, ['width', 'gap', 'iconSize']);

  const { label, desc, icon } = datum;

  const getTextAlign = (position: string) => {
    return position === 'normal'
      ? 'left'
      : position === 'flipped'
        ? 'right'
        : 'center';
  };

  const textAlign = getTextAlign(positionH);

  const labelContent = (
    <ItemLabel
      indexes={indexes}
      width={width}
      alignHorizontal="center"
      alignVertical="center"
    >
      {label}
    </ItemLabel>
  );
  const labelBounds = getElementBounds(labelContent);
  const iconContent = <ItemIcon indexes={indexes} size={iconSize} />;

  if (!icon) {
    return (
      <Group {...restProps}>
        <ItemLabel
          indexes={indexes}
          width={width}
          alignHorizontal={textAlign}
          alignVertical="center"
        >
          {label}
        </ItemLabel>
        <ItemDesc
          indexes={indexes}
          width={width}
          y={labelBounds.height + gap}
          alignHorizontal={textAlign}
          alignVertical={getDescVerticalAlign(positionV, false)}
        >
          {desc}
        </ItemDesc>
      </Group>
    );
  }

  if (positionH === 'center') {
    return (
      <FlexLayout
        {...restProps}
        flexDirection="column"
        gap={gap}
        alignItems="center"
      >
        {positionV === 'flipped' ? (
          <>
            <Group>
              {labelContent}
              <ItemDesc
                indexes={indexes}
                width={width}
                y={labelBounds.height + gap}
                alignHorizontal="center"
                alignVertical="bottom"
              >
                {desc}
              </ItemDesc>
            </Group>
            {iconContent}
          </>
        ) : (
          <>
            {iconContent}
            <Group>
              {labelContent}
              <ItemDesc
                indexes={indexes}
                width={width}
                y={labelBounds.height + gap}
                alignHorizontal="center"
                alignVertical="top"
              >
                {desc}
              </ItemDesc>
            </Group>
          </>
        )}
      </FlexLayout>
    );
  }

  const iconBounds = getElementBounds(iconContent);
  const textWidth = Math.max(width - iconBounds.width - gap, 0);

  return (
    <FlexLayout
      {...restProps}
      flexDirection="row"
      gap={gap}
      alignItems={getIconVerticalAlign(positionV)}
    >
      {positionH === 'flipped' ? (
        <>
          <Group>
            <ItemLabel
              indexes={indexes}
              width={textWidth}
              alignHorizontal="right"
              alignVertical="center"
            >
              {label}
            </ItemLabel>
            <ItemDesc
              indexes={indexes}
              width={textWidth}
              y={labelBounds.height + gap}
              alignHorizontal="right"
              alignVertical={getDescVerticalAlign(positionV, true)}
            >
              {desc}
            </ItemDesc>
          </Group>
          {iconContent}
        </>
      ) : (
        <>
          {iconContent}
          <Group>
            <ItemLabel
              indexes={indexes}
              width={textWidth}
              alignHorizontal="left"
              alignVertical="center"
            >
              {label}
            </ItemLabel>
            <ItemDesc
              indexes={indexes}
              width={textWidth}
              y={labelBounds.height + gap}
              alignHorizontal="left"
              alignVertical={getDescVerticalAlign(positionV, true)}
            >
              {desc}
            </ItemDesc>
          </Group>
        </>
      )}
    </FlexLayout>
  );

  function getDescVerticalAlign(positionV: string, hasIcon: boolean) {
    return 'top';
    // if (positionV === 'normal') return 'top';
    // if (positionV === 'flipped') return 'bottom';

    return hasIcon ? 'center' : 'top';
  }

  function getIconVerticalAlign(positionV: string) {
    if (positionV === 'normal') return 'flex-start';
    if (positionV === 'flipped') return 'flex-end';
    return 'center';
  }
};

registerItem('simple', { component: SimpleItem });
