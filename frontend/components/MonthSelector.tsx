'use client';

import React from 'react';

const monthLabels = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
];

interface Props {
  availableMonths: number[];
  selectedMonth: number | null;
  onChange: (month: number) => void;
}

export default function MonthSelector({ availableMonths, selectedMonth, onChange }: Props) {
  return (
    <div className="p-4">
      <label className="block text-sm font-medium text-gray-700" htmlFor="month-select">
        Select month
      </label>
      <select
        id="month-select"
        className="mt-2 block w-full rounded-md border border-gray-300 bg-white p-2"
        value={selectedMonth ?? ''}
        onChange={(e) => onChange(Number(e.target.value))}
      >
        <option value="" disabled>
          Choose...
        </option>
        {availableMonths.map((m) => (
          <option key={m} value={m}>
            {monthLabels[m - 1] ?? `Month ${m}`}
          </option>
        ))}
      </select>
    </div>
  );
}
