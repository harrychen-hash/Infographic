import { getTemplates } from '@antv/infographic';
import { Checkbox, Flex, Form, Select } from 'antd';
import { useEffect, useState } from 'react';
import { Infographic } from './Infographic';
import { COMPARE_DATA, HIERARCHY_DATA, LIST_DATA } from './data';
import { getSearchParam, setSearchParam } from './utils/search-params';

const templates = getTemplates();

const DATA = {
  list: { label: '列表数据', value: LIST_DATA },
  hierarchy: { label: '层级数据', value: HIERARCHY_DATA },
  compare: { label: '对比数据', value: COMPARE_DATA },
} as const;

export const Preview = () => {
  const [template, setTemplate] = useState(
    getSearchParam('template') || templates[0],
  );
  const [themeConfig, setThemeConfig] = useState({});
  const [data, setData] = useState<keyof typeof DATA>('list');

  useEffect(() => {
    if (template.startsWith('hierarchy-')) {
      setData('hierarchy');
    } else if (template.startsWith('compare-')) {
      setData('compare');
    } else {
      setData('list');
    }
  }, [template]);

  return (
    <Flex vertical>
      <Form layout="inline">
        <Form.Item label="模板">
          <Select
            value={template}
            style={{ minWidth: 200 }}
            options={templates.map((value) => ({ label: value, value }))}
            onChange={(value) => {
              setTemplate(value);
              setSearchParam('template', value);
            }}
          />
        </Form.Item>
        <Form.Item label="数据">
          <Select
            value={data}
            style={{ width: 100 }}
            options={Object.entries(DATA).map(([key, { label }]) => ({
              label,
              value: key,
            }))}
            onChange={(value) => setData(value)}
          />
        </Form.Item>
        <Form.Item label="主题" name="theme">
          <Select
            style={{ width: 80 }}
            defaultValue="light"
            options={[
              { label: '亮色', value: 'light' },
              { label: '暗色', value: 'dark' },
            ]}
            onChange={(theme) => {
              setThemeConfig((pre) => ({
                ...pre,
                colorBg: theme === 'dark' ? '#333' : '#fff',
              }));
            }}
          />
        </Form.Item>
        <Form.Item name="enablePalette" valuePropName="checked">
          <Checkbox
            onChange={(e) => {
              const enablePalette = e.target.checked;
              setThemeConfig((pre) => ({
                ...pre,
                palette: enablePalette
                  ? [
                      '#1783FF',
                      '#00C9C9',
                      '#F0884D',
                      '#D580FF',
                      '#7863FF',
                      '#60C42D',
                      '#BD8F24',
                      '#FF80CA',
                      '#2491B3',
                      '#17C76F',
                      '#70CAF8',
                    ]
                  : [],
              }));
            }}
          >
            启用色板
          </Checkbox>
        </Form.Item>
      </Form>
      <Infographic
        options={{
          template,
          data: DATA[data].value,
          padding: 20,
          themeConfig,
        }}
      />
    </Flex>
  );
};
