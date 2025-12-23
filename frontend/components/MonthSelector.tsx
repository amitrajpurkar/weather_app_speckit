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
  const isDisabled = availableMonths.length === 0;

  return (
    <div className="p-4">
      <label className="block text-sm font-medium text-gray-700" htmlFor="month-select">
        Select month
      </label>
      <select
        id="month-select"
        className="mt-2 block w-full rounded-md border border-gray-300 bg-white p-2"
        disabled={isDisabled}
        value={selectedMonth ?? ''}
        onChange={(e) => onChange(Number(e.target.value))}
      >
        <option value="" disabled>
          {isDisabled ? 'No months available' : 'Choose...'}
        </option>
        {availableMonths.map((m) => (
          <option key={m} value={m}>
            {monthLabels[m - 1] ?? `Month ${m}`}
          </option>
        ))}
      </select>

      {isDisabled && (
        <div className="mt-2 text-sm text-gray-600">
          No months with data are available for the selected year.
        </div>
      )}
    </div>
  );
}
