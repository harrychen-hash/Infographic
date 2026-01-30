/**
 * [INPUT]: (data, options) - 组合图数据，包含 primaryItems (柱状图) 和 secondaryItems (折线图)
 * [OUTPUT]: JSXElement - 渲染包含柱状图+折线图的组合图 SVG
 * [POS]: 实验性组件，验证双轴组合图渲染可行性
 *
 * [PROTOCOL]:
 * 1. 一旦本文件逻辑变更，必须同步更新此 Header。
 * 2. 更新后必须上浮检查 /src/designs/structures/.folder.md 的描述是否仍然准确。
 */

import { scaleLinear } from 'd3';
import tinycolor from 'tinycolor2';
import type { ComponentType, JSXElement } from '../../jsx';
import { Defs, Ellipse, Group, Path, Rect, Text } from '../../jsx';
import { ItemDatum, Padding } from '../../types';
import { parsePadding } from '../../utils';
import { FlexLayout } from '../layouts';
import { getPaletteColor, getThemeColors } from '../utils';
import { registerStructure } from './registry';
import type { BaseStructureProps } from './types';

export interface ChartComboProps extends BaseStructureProps {
  columnWidth?: number;
  columnGap?: number;
  padding?: Padding;
  showValue?: boolean;
  valueFormatter?: (value: number, datum: ItemDatum) => string;
}

// 硬编码测试数据 - 验证渲染可行性
// 实际使用时，这些数据应从 DSL 传入
const HARDCODED_PRIMARY = [
  { label: 'Q1', value: 100 },
  { label: 'Q2', value: 150 },
  { label: 'Q3', value: 120 },
  { label: 'Q4', value: 200 },
];

const HARDCODED_SECONDARY = [
  { label: 'Q1', value: 10 },
  { label: 'Q2', value: 25 },
  { label: 'Q3', value: 15 },
  { label: 'Q4', value: 35 },
];

export const ChartCombo: ComponentType<ChartComboProps> = (props) => {
  const {
    Title,
    data,
    columnWidth = 40,
    columnGap = 60,
    padding = 40,
    showValue = true,
    options,
    valueFormatter = (value) => value.toString(),
  } = props;

  const {
    title,
    desc,
    primaryValues: dataPrimary,
    secondaryValues: dataSecondary,
    xTitle,
    primaryYTitle,
    secondaryYTitle,
    primaryLabel = '销售额 (左轴)',
    secondaryLabel = '增长率 % (右轴)',
    // 坐标轴参数
    primaryMin,
    primaryMax: userPrimaryMax,
    primaryStep,
    secondaryMin,
    secondaryMax: userSecondaryMax,
    secondaryStep,
  } = data as {
    title?: string;
    desc?: string;
    primaryValues?: { label: string; value: number }[];
    secondaryValues?: { label: string; value: number }[];
    xTitle?: string;
    primaryYTitle?: string;
    secondaryYTitle?: string;
    primaryLabel?: string;
    secondaryLabel?: string;
    // 坐标轴参数类型
    primaryMin?: number;
    primaryMax?: number;
    primaryStep?: number;
    secondaryMin?: number;
    secondaryMax?: number;
    secondaryStep?: number;
  };
  const titleContent = Title ? <Title title={title} desc={desc} /> : null;

  // 从 DSL 读取数据，fallback 到硬编码测试数据
  const primaryItems = dataPrimary?.length ? dataPrimary : HARDCODED_PRIMARY;
  const secondaryItems = dataSecondary?.length ? dataSecondary : HARDCODED_SECONDARY;

  const themeColors = getThemeColors(options.themeConfig);

  // 图表尺寸
  const chartWidth = primaryItems.length * columnWidth + (primaryItems.length - 1) * columnGap;
  const chartHeight = 280;
  const [paddingTop, paddingRight, paddingBottom, paddingLeft] = parsePadding(padding);

  // 为轴标签留出空间
  const rightAxisSpace = 50;
  const leftAxisSpace = 50;
  const xLabelSpace = 40;
  const legendSpace = 30;

  // 轴标题空间
  const xTitleSpace = xTitle ? 22 : 0;
  const primaryYTitleSpace = primaryYTitle ? 26 : 0;
  const secondaryYTitleSpace = secondaryYTitle ? 26 : 0;

  const totalWidth = primaryYTitleSpace + leftAxisSpace + chartWidth + rightAxisSpace + secondaryYTitleSpace + paddingLeft + paddingRight;
  const totalHeight = chartHeight + paddingTop + paddingBottom + xLabelSpace + xTitleSpace + legendSpace;

  // 左 Y 轴比例尺 (柱状图)
  const primaryValuesArr = primaryItems.map((item) => item.value ?? 0);
  const primaryDataMax = Math.max(...primaryValuesArr, 0);
  const primaryDomainMin = primaryMin ?? 0;
  const primaryDomainMax = userPrimaryMax ?? primaryDataMax * 1.15;

  const scaleYLeft = scaleLinear()
    .domain([primaryDomainMin, primaryDomainMax])
    .nice()
    .range([chartHeight, 0]);

  // 右 Y 轴比例尺 (折线图) - 允许与柱状图重叠
  const secondaryValuesArr = secondaryItems.map((item) => item.value ?? 0);
  const secondaryDataMax = Math.max(...secondaryValuesArr, 0);
  const secondaryDomainMin = secondaryMin ?? 0;
  const secondaryDomainMax = userSecondaryMax ?? secondaryDataMax * 1.15;

  const scaleYRight = scaleLinear()
    .domain([secondaryDomainMin, secondaryDomainMax])
    .nice()
    .range([chartHeight, 0]);

  const chartOriginX = paddingLeft + primaryYTitleSpace + leftAxisSpace;
  const chartOriginY = paddingTop;

  const gridElements: JSXElement[] = [];
  const axisElements: JSXElement[] = [];
  const columnElements: JSXElement[] = [];
  const lineElements: JSXElement[] = [];
  const pointElements: JSXElement[] = [];
  const valueElements: JSXElement[] = [];
  const tickElements: JSXElement[] = [];
  const labelElements: JSXElement[] = [];
  const gradientDefs: JSXElement[] = [];
  const titleElements: JSXElement[] = [];

  const axisColor = themeColors.colorText || '#666';
  const columnColor = getPaletteColor(options, [0]) || '#21EF6A';
  const lineColor = getPaletteColor(options, [1]) || '#FF6B6B';

  // 生成刻度数组的辅助函数
  const generateTicks = (min: number, max: number, step?: number, defaultCount = 5): number[] => {
    if (step && step > 0) {
      const ticks: number[] = [];
      for (let v = min; v <= max; v += step) {
        ticks.push(Math.round(v * 1000) / 1000); // 避免浮点精度问题
      }
      return ticks;
    }
    // 默认使用 d3 的 ticks
    return scaleLinear().domain([min, max]).ticks(defaultCount);
  };

  // 网格线
  const ticksYLeft = generateTicks(primaryDomainMin, primaryDomainMax, primaryStep);
  ticksYLeft.forEach((tick) => {
    const yPos = chartOriginY + scaleYLeft(tick);
    gridElements.push(
      <Path
        d={`M ${chartOriginX} ${yPos} L ${chartOriginX + chartWidth} ${yPos}`}
        width={chartWidth}
        height={1}
        stroke={axisColor}
        strokeWidth={1}
        opacity={0.1}
        data-element-type="shape"
      />,
    );
  });

  // 左 Y 轴 (柱状图)
  axisElements.push(
    <Path
      d={`M ${chartOriginX} ${chartOriginY} L ${chartOriginX} ${chartOriginY + chartHeight}`}
      width={1}
      height={chartHeight}
      stroke={columnColor}
      strokeWidth={2}
      data-element-type="shape"
    />,
  );

  // 左轴刻度
  ticksYLeft.forEach((tick) => {
    const yPos = chartOriginY + scaleYLeft(tick);
    tickElements.push(
      <Text
        x={chartOriginX - 8}
        y={yPos}
        alignHorizontal="right"
        alignVertical="middle"
        fontSize={11}
        fill={columnColor}
      >
        {tick.toString()}
      </Text>,
    );
  });

  // 右 Y 轴 (折线图)
  axisElements.push(
    <Path
      d={`M ${chartOriginX + chartWidth} ${chartOriginY} L ${chartOriginX + chartWidth} ${chartOriginY + chartHeight}`}
      width={1}
      height={chartHeight}
      stroke={lineColor}
      strokeWidth={2}
      data-element-type="shape"
    />,
  );

  // 右轴刻度
  const ticksYRight = generateTicks(secondaryDomainMin, secondaryDomainMax, secondaryStep);
  ticksYRight.forEach((tick) => {
    const yPos = chartOriginY + scaleYRight(tick);
    tickElements.push(
      <Text
        x={chartOriginX + chartWidth + 8}
        y={yPos}
        alignHorizontal="left"
        alignVertical="middle"
        fontSize={11}
        fill={lineColor}
      >
        {tick.toString()}
      </Text>,
    );
  });

  // X 轴
  axisElements.push(
    <Path
      d={`M ${chartOriginX} ${chartOriginY + chartHeight} L ${chartOriginX + chartWidth} ${chartOriginY + chartHeight}`}
      width={chartWidth}
      height={1}
      stroke={axisColor}
      strokeWidth={1}
      data-element-type="shape"
    />,
  );

  // 渲染柱状图
  primaryItems.forEach((item, index) => {
    const value = item.value ?? 0;
    const columnX = chartOriginX + index * (columnWidth + columnGap);
    const columnY = scaleYLeft(value);
    const zeroY = scaleYLeft(0);
    const columnHeight = zeroY - columnY;

    const gradientId = `combo-column-gradient-${index}`;
    gradientDefs.push(
      <linearGradient id={gradientId} x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stopColor={columnColor} />
        <stop offset="100%" stopColor={tinycolor.mix(columnColor, '#fff', 40).toHexString()} />
      </linearGradient>,
    );

    columnElements.push(
      <Rect
        x={columnX}
        y={chartOriginY + columnY}
        width={columnWidth}
        height={columnHeight}
        fill={`url(#${gradientId})`}
        rx={4}
        ry={4}
        data-element-type="shape"
      />,
    );

    // 柱状图值标签
    if (showValue) {
      valueElements.push(
        <Text
          x={columnX + columnWidth / 2}
          y={chartOriginY + columnY - 6}
          alignHorizontal="center"
          alignVertical="bottom"
          fontSize={11}
          fontWeight="bold"
          fill={columnColor}
        >
          {valueFormatter(value, item)}
        </Text>,
      );
    }

    // X 轴标签
    labelElements.push(
      <Text
        x={columnX + columnWidth / 2}
        y={chartOriginY + chartHeight + 16}
        alignHorizontal="center"
        alignVertical="top"
        fontSize={12}
        fill={axisColor}
      >
        {item.label || ''}
      </Text>,
    );
  });

  // 渲染折线图
  const linePoints: { x: number; y: number }[] = [];
  secondaryItems.forEach((item, index) => {
    const x = chartOriginX + index * (columnWidth + columnGap) + columnWidth / 2;
    const y = chartOriginY + scaleYRight(item.value ?? 0);
    linePoints.push({ x, y });
  });

  // 创建平滑曲线路径
  const createSmoothPath = (points: { x: number; y: number }[]) => {
    if (points.length === 0) return '';
    if (points.length === 1) return `M ${points[0].x} ${points[0].y}`;

    const segments: string[] = [];
    segments.push(`M ${points[0].x} ${points[0].y}`);

    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[i - 1] || points[i];
      const p1 = points[i];
      const p2 = points[i + 1];
      const p3 = points[i + 2] || p2;

      const cp1x = p1.x + (p2.x - p0.x) / 6;
      const cp1y = p1.y + (p2.y - p0.y) / 6;
      const cp2x = p2.x - (p3.x - p1.x) / 6;
      const cp2y = p2.y - (p3.y - p1.y) / 6;

      segments.push(`C ${cp1x} ${cp1y} ${cp2x} ${cp2y} ${p2.x} ${p2.y}`);
    }

    return segments.join(' ');
  };

  const linePath = createSmoothPath(linePoints);

  // 折线渐变
  const lineGradientId = 'combo-line-gradient';
  gradientDefs.push(
    <linearGradient id={lineGradientId} x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stopColor={lineColor} />
      <stop offset="100%" stopColor={tinycolor.mix(lineColor, '#fff', 20).toHexString()} />
    </linearGradient>,
  );

  lineElements.push(
    <Path
      d={linePath}
      width={chartWidth}
      height={chartHeight}
      stroke={`url(#${lineGradientId})`}
      strokeWidth={3}
      fill="none"
      data-element-type="shape"
    />,
  );

  // 折线图数据点
  linePoints.forEach((pos, index) => {
    pointElements.push(
      <Ellipse
        x={pos.x - 5}
        y={pos.y - 5}
        width={10}
        height={10}
        fill={lineColor}
        data-element-type="shape"
      />,
    );

    // 折线图值标签
    if (showValue) {
      valueElements.push(
        <Text
          x={pos.x}
          y={pos.y - 12}
          alignHorizontal="center"
          alignVertical="bottom"
          fontSize={10}
          fontWeight="bold"
          fill={lineColor}
        >
          {valueFormatter(secondaryItems[index].value ?? 0, secondaryItems[index])}
        </Text>,
      );
    }
  });

  // 轴标题
  if (xTitle) {
    titleElements.push(
      <Text
        x={chartOriginX + chartWidth / 2}
        y={chartOriginY + chartHeight + xLabelSpace + xTitleSpace / 2}
        alignHorizontal="center"
        alignVertical="middle"
        fontSize={14}
        fontWeight="bold"
        fill={axisColor}
      >
        {xTitle}
      </Text>,
    );
  }

  if (primaryYTitle) {
    titleElements.push(
      <Text
        x={paddingLeft + primaryYTitleSpace / 2}
        y={chartOriginY + chartHeight / 2}
        alignHorizontal="center"
        alignVertical="middle"
        fontSize={14}
        fontWeight="bold"
        fill={columnColor}
      >
        {primaryYTitle}
      </Text>,
    );
  }

  if (secondaryYTitle) {
    titleElements.push(
      <Text
        x={chartOriginX + chartWidth + rightAxisSpace + secondaryYTitleSpace / 2}
        y={chartOriginY + chartHeight / 2}
        alignHorizontal="center"
        alignVertical="middle"
        fontSize={14}
        fontWeight="bold"
        fill={lineColor}
      >
        {secondaryYTitle}
      </Text>,
    );
  }

  // 图例
  const legendY = chartOriginY + chartHeight + xLabelSpace + xTitleSpace + 6;
  const legendElements: JSXElement[] = [
    // 柱状图图例
    <Rect
      x={chartOriginX}
      y={legendY}
      width={12}
      height={12}
      fill={columnColor}
      rx={2}
      data-element-type="shape"
    />,
    <Text
      x={chartOriginX + 16}
      y={legendY + 6}
      alignHorizontal="left"
      alignVertical="middle"
      fontSize={11}
      fill={axisColor}
    >
      {primaryLabel}
    </Text>,
    // 折线图图例
    <Path
      d={`M ${chartOriginX + 100} ${legendY + 6} L ${chartOriginX + 120} ${legendY + 6}`}
      width={20}
      height={2}
      stroke={lineColor}
      strokeWidth={3}
      data-element-type="shape"
    />,
    <Ellipse
      x={chartOriginX + 105}
      y={legendY + 1}
      width={10}
      height={10}
      fill={lineColor}
      data-element-type="shape"
    />,
    <Text
      x={chartOriginX + 126}
      y={legendY + 6}
      alignHorizontal="left"
      alignVertical="middle"
      fontSize={11}
      fill={axisColor}
    >
      {secondaryLabel}
    </Text>,
  ];

  return (
    <FlexLayout
      id="infographic-container"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
    >
      {titleContent}
      <Group width={totalWidth} height={totalHeight}>
        <Defs>{gradientDefs}</Defs>
        <Group>{gridElements}</Group>
        <Group>{axisElements}</Group>
        <Group>{tickElements}</Group>
        <Group>{columnElements}</Group>
        <Group>{lineElements}</Group>
        <Group>{pointElements}</Group>
        <Group>{valueElements}</Group>
        <Group>{labelElements}</Group>
        <Group>{titleElements}</Group>
        <Group>{legendElements}</Group>
      </Group>
    </FlexLayout>
  );
};

registerStructure('chart-combo', {
  component: ChartCombo,
  composites: ['title', 'item', 'xTitle', 'primaryYTitle', 'secondaryYTitle'],
});
